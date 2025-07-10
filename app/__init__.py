import os
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder="templates")
    
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'uploads')
    app.config['OUTPUT_FOLDER'] = os.path.join(base_dir, 'outputs')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
    app.secret_key = 'supersecret'

    from app.routes import main
    app.register_blueprint(main)

    return app
