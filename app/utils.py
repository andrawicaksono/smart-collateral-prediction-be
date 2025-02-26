import bleach
import hmac
import hashlib
from .config import Config

def sanitize_input(data):
    """Sanitize input data to prevent XSS attacks."""
    if isinstance(data, dict):
        return {k: bleach.clean(str(v)) for k, v in data.items()}
    elif isinstance(data, list):
        return [bleach.clean(str(v)) for v in data]
    elif isinstance(data, str):
        return bleach.clean(data)
    return data

def generate_hmac_signature(api_key, timestamp, payload):
    """Generate HMAC SHA256 signature."""
    message = f"{api_key}:{timestamp}:{payload}".encode()
    return hmac.new(Config.SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()

def verify_hmac_signature(api_key, timestamp, payload, provided_signature):
    """Verify HMAC SHA256 signature."""
    expected_signature = generate_hmac_signature(api_key, timestamp, payload)
    return hmac.compare_digest(expected_signature, provided_signature)
