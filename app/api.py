# api.py
from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd
from flask_cors import CORS


# Initialize Flask app
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# Load the pre-trained model
model = joblib.load(r'C:\Users\mouad\car-price-predictor\src\car_price_model.pkl')

# Define the feature names in the order expected by the model
feature_names = [
    'Marque', 'Modèle', 'Année', 'Type de carburant', 'Puissance fiscale',
    'Kilométrage', 'Nombre de portes', 'Première main', 'État',
    'Boîte à vitesses', 'Origine'
]

# Vercel calls this
def handler(req):
    return app(req)

@app.route('/')
def home():
    return "🚗 Welcome to the Car Price Prediction API!"

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON request
        data = request.get_json()

        # Check if all required features are in the request
        missing = [feat for feat in feature_names if feat not in data]
        if missing:
            return jsonify({"error": f"Missing features: {missing}"}), 400

        # Create a DataFrame with one row
        input_df = pd.DataFrame([data])

        # Predict
        predicted_price = model.predict(input_df)[0]

        return jsonify({'predicted_price': round(float(predicted_price), 2)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
