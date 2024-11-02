import os
from flask import Flask, render_template
from flask_cors import CORS
from api.test import test_api
from api.peer import peer_api

def create_app():
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

    app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
    CORS(app)
    app.register_blueprint(test_api)
    app.register_blueprint(peer_api)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('index.html')

    return app