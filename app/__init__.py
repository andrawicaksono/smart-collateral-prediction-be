from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)

    from .config import Config
    app.config.from_object(Config)

    CORS(app, origins=[app.config["CORS_ORIGIN"]])

    from .routes import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/api/v1")

    return app
