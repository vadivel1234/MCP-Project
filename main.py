
import os
from flask import Flask, render_template, send_from_directory, Blueprint, jsonify, request
import flask_cors

# Resolve absolute paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BASE_DIR, 'build')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

app = Flask(
    __name__,
    static_folder=BUILD_DIR,        # serve static from build
    static_url_path='',             # so "/static" isn't prefixed; files in build can be served at "/..."
    template_folder=BUILD_DIR       # templates (index.html) inside build
)

flask_cors.CORS(app)

api = Blueprint("api", __name__, url_prefix="/api")


# Serve images from absolute images directory
@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)


# SPA routing: if a built asset exists, serve it; else serve index.html
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # Absolute path to requested file under build/
    requested_path = os.path.join(BUILD_DIR, path) if path else None

    # Serve the file directly if it exists
    if path and os.path.isfile(requested_path):
        # Use send_from_directory with absolute build dir
        return send_from_directory(BUILD_DIR, path)

    # Otherwise serve index.html (SPA fallback)
    return render_template('index.html')


# Fix API route (no arg) OR accept query param
@api.route('/simple-get', methods=['GET'])
def get_item():
    # Option A: return a fixed payload
    # return jsonify({"status": "ok"})

    # Option B: read from query param: /api/simple-get?name=Vadivel
    name = request.args.get('name', 'default')
    return jsonify({"name": name})


# Register blueprint
app.register_blueprint(api)


if __name__ == '__main__':
    print("Server started on http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)
