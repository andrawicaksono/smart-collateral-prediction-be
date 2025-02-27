from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

def create_app():
    load_dotenv()

    app = Flask(__name__)

    from .config import Config
    app.config.from_object(Config)

    CORS(app, origins=[app.config["CORS_ORIGIN"]])

    from .routes import main_blueprint
    app.register_blueprint(main_blueprint, url_prefix="/api/v1")

        
    # Swagger UI configuration
    SWAGGER_URL = "/api/v1/swagger"
    API_URL = "/swagger.json"

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Smart Collateral Prediction API"}
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route("/swagger.json")
    def swagger_json():
        return send_from_directory(".", "swagger.json")

    return app
