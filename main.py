import flask_cors
from flask import Flask, render_template, send_from_directory, Blueprint, jsonify
import os

app = Flask(__name__, static_folder='build', template_folder='build')
flask_cors.CORS(app)
api = Blueprint("api", __name__, url_prefix="/api")


@app.route('/images/<filename>')
def serve_image(filename):
    """Serve images from the images/ folder."""
    return send_from_directory('images', filename)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # If a static file under `build/` is requested, serve it directly.
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise serve the single-page `index.html`.
    return render_template('index.html')

@api.route('/simple-get', methods=['GET'])
def get_item(name):
    return jsonify(name)


if __name__ == '__main__':
    print("Server started on http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)