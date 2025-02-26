import logging
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, ValidationError
from .utils import sanitize_input, verify_hmac_signature
from .services import estimate_price
from .config import Config

main_blueprint = Blueprint("main", __name__)

class InputData(BaseModel):
    city: str
    latitude: float
    longitude: float
    land_size: int
    building_size: int
    floors: int
    electricity: int
    certificate: str
    property_condition: int
    bedrooms: int
    bathrooms: int
    swimming_pool: int
    garage: int
    carport: int
    garden: int
    drying_area: int
    security: int
    parking_access: int

@main_blueprint.route("/predict", methods=["POST"])
def predict():
    try:
        # provided_api_key = request.headers.get("X-API-KEY")
        # provided_timestamp = request.headers.get("X-TIMESTAMP")
        # provided_signature = request.headers.get("X-SIGNATURE")

        # if provided_api_key != Config.API_KEY:
        #     return jsonify({"error": "Unauthorized"}), 403

        # raw_data = request.get_data(as_text=True)
        # if not verify_hmac_signature(provided_api_key, provided_timestamp, raw_data, provided_signature):
        #     return jsonify({"error": "Invalid credentials"}), 403

        json_data = request.get_json()
        sanitized_data = sanitize_input(json_data)
        input_data = InputData(**sanitized_data)

        prediction = estimate_price(input_data)

        return jsonify({
            "success": True,
            "message": "Prediction successful",
            "data": float(prediction)
        }), 200

    except ValidationError as e:
        return jsonify({"error": "Invalid input", "details": e.errors()}), 400
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
