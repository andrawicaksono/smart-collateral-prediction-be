import os
import pickle
import logging
import hmac
import hashlib
import bleach
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY", "my_secure_api_key")
HMAC_SECRET = os.getenv("HMAC_SECRET", "my_hmac_secret_key")
CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")

app = Flask(__name__)

CORS(app, origins=[CORS_ORIGIN]) 

MODEL_PATH = "models/xgb_model_select1.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

class InputData(BaseModel):
    city: str
    latitude: float
    longitude: float
    land_size: int
    building_size: int
    floor: int
    electricity: int
    certificate: str
    property_condition: int
    bedroom: int
    bathroom: int
    swimming_pool: int
    garage: int
    carport: int
    garden: int
    drying_area: int
    security: int
    parking_access: int

def sanitize_input(data):
    """Sanitize input to prevent XSS attacks."""
    if isinstance(data, dict):
        return {k: bleach.clean(str(v)) for k, v in data.items()}
    elif isinstance(data, list):
        return [bleach.clean(str(v)) for v in data]
    elif isinstance(data, str):
        return bleach.clean(data)
    return data

def generate_hmac_signature(api_key, timestamp, payload):
    """Generate HMAC SHA256 signature."""
    message = f"{api_key}{timestamp}{payload}".encode()
    return hmac.new(HMAC_SECRET.encode(), message, hashlib.sha256).hexdigest()

def verify_hmac_signature(api_key, timestamp, payload, provided_signature):
    """Verify HMAC SHA256 signature."""
    expected_signature = generate_hmac_signature(api_key, timestamp, payload)
    return hmac.compare_digest(expected_signature, provided_signature)

def estimate_price(latitude, longitude, land_size, building_size, floor, electricity, 
                   property_condition, bedroom, bathroom, swimming_pool, garage, carport, 
                   garden, drying_area, security, parking_access, certificate, city):
    
    # Create input DataFrame
    df = pd.DataFrame([{
        'latitude': latitude, 'longitude': longitude, 'land_size': land_size, 'building_size': building_size, 
        'floor': floor, 'electricity': electricity, 'property_condition': property_condition, 'bedroom': bedroom, 
        'bathroom': bathroom, 'swimming_pool': swimming_pool, 'garage': garage, 'carport': carport, 'garden': garden, 
        'drying_area': drying_area, 'security': security, 'parking_access': parking_access
    }])
    
    # One-hot encoding for 'certificate'
    certificate_categories = ['SHM', 'SHGB', 'SHP', 'Lainnya']
    df = df.assign(**{f'certificate_{cat}': int(certificate == cat) for cat in certificate_categories})

    # One-hot encoding for 'city'
    city_categories = [
        'bekasi', 'bogor', 'depok', 'jakarta barat', 'jakarta pusat', 
        'jakarta selatan', 'jakarta timur', 'jakarta utara', 'tangerang'
    ]
    df = df.assign(**{f'city_{c}': int(city.lower() == c) for c in city_categories})

    # Add building-to-land ratio
    df['building_to_land_ratio'] = building_size / land_size

    # Predict using the model
    prediction = model.predict(df)

    return prediction[0]

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # provided_api_key = request.headers.get("X-API-KEY")
        # provided_timestamp = request.headers.get("X-TIMESTAMP")
        # provided_signature = request.headers.get("X-SIGNATURE")

        # if provided_api_key != API_KEY:
        #     return jsonify({"error": "Unauthorized"}), 403

        # raw_data = request.get_data(as_text=True)
        # if not verify_hmac_signature(provided_api_key, provided_timestamp, raw_data, provided_signature):
        #     return jsonify({"error": "Invalid credentials"}), 403

        json_data = request.get_json()
        sanitized_data = sanitize_input(json_data)
        input_data = InputData(**sanitized_data)

        prediction = estimate_price(
            latitude=input_data.latitude,
            longitude=input_data.longitude,
            land_size=input_data.land_size,
            building_size=input_data.building_size,
            floor=input_data.floor,
            electricity=input_data.electricity,
            property_condition=input_data.property_condition,
            bedroom=input_data.bedroom,
            bathroom=input_data.bathroom,
            swimming_pool=input_data.swimming_pool,
            garage=input_data.garage,
            carport=input_data.carport,
            garden=input_data.garden,
            drying_area=input_data.drying_area,
            security=input_data.security,
            parking_access=input_data.parking_access,
            certificate=input_data.certificate,
            city=input_data.city
        )

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

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
