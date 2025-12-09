from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, static_folder='build', template_folder='build')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    # If a static file under `build/` is requested, serve it directly.
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise serve the single-page `index.html`.
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)