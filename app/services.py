import pickle
import pandas as pd
from .config import Config

with open(Config.MODEL_PATH, "rb") as file:
    model = pickle.load(file)

def estimate_price(data):
    """Predict property price based on input features."""

    df = pd.DataFrame([{
        'latitude': data.latitude,
        'longitude': data.longitude,
        'land_size': data.land_size,
        'building_size': data.building_size,
        'floor': data.floor,
        'electricity': data.electricity,
        'property_condition': data.property_condition,
        'bedroom': data.bedroom,
        'bathroom': data.bathroom,
        'swimming_pool': data.swimming_pool,
        'garage': data.garage,
        'carport': data.carport,
        'garden': data.garden,
        'drying_area': data.drying_area,
        'security': data.security,
        'parking_access': data.parking_access
    }])

    # One-hot encoding for 'certificate'
    certificate_categories = ['SHM', 'SHGB', 'SHP', 'Lainnya']
    for cat in certificate_categories:
        df[f'certificate_{cat}'] = int(data.certificate == cat)

    # One-hot encoding for 'city'
    city_categories = [
        'bekasi', 'bogor', 'depok', 'jakarta barat', 'jakarta pusat', 
        'jakarta selatan', 'jakarta timur', 'jakarta utara', 'tangerang'
    ]
    for city in city_categories:
        df[f'city_{city}'] = int(data.city.lower() == city)

    df['building_to_land_ratio'] = data.building_size / data.land_size

    prediction = model.predict(df)

    return prediction[0]
