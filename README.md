# Smart Collateral Prediction API

The **Smart Collateral Prediction API** provides a RESTful service for predicting property prices based on various input features such as location, building size, land size, and other property details. This API includes authentication via API keys, input validation, and HMAC signature verification for added security.

---

## Table of Contents

- [Features](#features)
- [API Endpoints](#api-endpoints)
  - [Check API Health](#check-api-health)
  - [Predict Property Price](#predict-property-price)
- [Authentication](#authentication)
- [Input Data Schema](#input-data-schema)
- [Environment Variables](#environment-variables)
- [Running Locally](#running-locally)
- [Docker Setup](#docker-setup)

---

## Features

- **Health Check**: A simple endpoint to check if the API is running.
- **Property Price Prediction**: Predicts the price of a property based on input data like city, size, amenities, etc.
- **Swagger UI**: Interactive API documentation and testing interface at `/api/v1/swagger`.

---

## API Endpoints

### Check API Health

**Endpoint**: `/api/v1/check`  
**Method**: `GET`  
**Description**: Returns the health status of the API.

#### Example Response:

```json
{
  "success": true,
  "message": "OK"
}
```

---

### Predict Property Price

**Endpoint**: `/api/v1/predict`  
**Method**: `POST`  
**Description**: Predicts the price of a property based on input features.

#### Headers:

- `X-API-KEY`: Your API key for authentication.
- `X-TIMESTAMP`: The timestamp of the request.
- `X-SIGNATURE`: The HMAC SHA256 signature of the request payload.

#### Request Body Schema (JSON):

```json
{
  "city": "jakarta pusat",
  "latitude": -6.2088,
  "longitude": 106.8456,
  "land_size": 100,
  "building_size": 120,
  "floors": 2,
  "electricity": 1,
  "certificate": "SHM",
  "property_condition": 3,
  "bedrooms": 3,
  "bathrooms": 2,
  "swimming_pool": 1,
  "garage": 1,
  "carport": 1,
  "garden": 1,
  "drying_area": 1,
  "security": 1,
  "parking_access": 1
}
```

#### Example Response:

```json
{
  "success": true,
  "message": "Prediction successful",
  "data": 500000000.0
}
```

#### Error Responses:

- **400** - Invalid input
- **403** - Unauthorized or Invalid credentials
- **500** - Internal server error

---

## Authentication

The API uses an **API Key** for authentication. The API key must be sent in the request header as `X-API-KEY`. Additionally, every request requires an **HMAC signature** for security.

To generate an HMAC signature:

```python
import hmac
import hashlib

def generate_hmac_signature(api_key, timestamp, payload, secret_key):
    message = f"{api_key}:{timestamp}:{payload}".encode()
    return hmac.new(secret_key.encode(), message, hashlib.sha256).hexdigest()
```

The signature should be calculated using the request's payload, timestamp, and API key, and then sent as the `X-SIGNATURE` header.

---

## Input Data Schema

The following fields are required when submitting a request to the `/predict` endpoint:

- `city`: The city where the property is located.
- `latitude`: Latitude of the property.
- `longitude`: Longitude of the property.
- `land_size`: Size of the land in square meters.
- `building_size`: Size of the building in square meters.
- `floors`: Number of floors in the property.
- `electricity`: 1 if electricity is available, else 0.
- `certificate`: Property certificate type (e.g., SHM, SHGB, etc.).
- `property_condition`: Condition of the property (1-5 scale).
- `bedrooms`: Number of bedrooms.
- `bathrooms`: Number of bathrooms.
- `swimming_pool`: 1 if the property has a swimming pool, else 0.
- `garage`: 1 if the property has a garage, else 0.
- `carport`: 1 if the property has a carport, else 0.
- `garden`: 1 if the property has a garden, else 0.
- `drying_area`: 1 if the property has a drying area, else 0.
- `security`: 1 if the property has security, else 0.
- `parking_access`: 1 if the property has parking access, else 0.

---

## Environment Variables

You must configure the following environment variables in a `.env` file:

```env
API_KEY=your_api_key
SECRET_KEY=your_hmac_secret_key
CORS_ORIGIN=*
PORT=5000
```

---

## Running Locally

1. Clone the repository:

```bash
git clone https://github.com/yourusername/smart-collateral-prediction-api.git
cd smart-collateral-prediction-api
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables in a `.env` file:

```bash
cp .env.example .env
```

Edit the `.env` file and set your values.

4. Run the application:

```bash
python main.py
```

The application will be accessible at `http://localhost:5000`.

---

## Docker Setup

To run the application in a Docker container:

1. Build the Docker image:

```bash
docker-compose build
```

2. Start the container:

```bash
docker-compose up
```

This will start the Flask app, and it will be accessible at `http://localhost:5000`.

---
