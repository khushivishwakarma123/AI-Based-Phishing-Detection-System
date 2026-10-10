from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

from feature_extraction import extract_features


app = Flask(__name__)

# Load trained model
model = joblib.load("models/best_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "error": "Please enter a URL."
        }), 400

    # Extract URL features
    features = extract_features(url)

    # Convert to DataFrame
    feature_df = pd.DataFrame([features])

    # Make prediction
    prediction = model.predict(feature_df)[0]

    # Get probability
    probability = model.predict_proba(feature_df)[0]

    phishing_probability = probability[1] * 100

    if prediction == 1:
        result = "Phishing"
    else:
        result = "Legitimate"

    return jsonify({
    "url": url,
    "result": result,
    "confidence": round(
        max(probability) * 100,
        2
    ),
    "features": features
})

if __name__ == "__main__":
    app.run(debug=True)