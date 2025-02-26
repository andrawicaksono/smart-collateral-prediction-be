import os

class Config:
    API_KEY = os.getenv("API_KEY", "my_secure_api_key")
    SECRET_KEY = os.getenv("SECRET_KEY", "my_hmac_secret_key")
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "*")
    MODEL_PATH = "models/xgb_model_select1.pkl"
