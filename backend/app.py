import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

print("Loading ExtraaLearn lead conversion model...")
model = joblib.load("extraaLearn_lead_prediction_model_v1_0.joblib")
print("Model loaded successfully.")

FEATURE_ORDER = [
    "age",
    "current_occupation",
    "first_interaction",
    "profile_completed",
    "website_visits",
    "time_spent_on_website",
    "page_views_per_visit",
    "last_activity",
    "print_media_type1",
    "print_media_type2",
    "digital_media",
    "educational_channels",
    "referral",
]


@app.get("/")
def home():
    return "Welcome to the ExtraaLearn Lead Conversion Prediction API!"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/v1/predict")
def predict_lead():
    data = request.get_json(force=True)
    input_data = pd.DataFrame([{col: data[col] for col in FEATURE_ORDER}])
    prediction = int(model.predict(input_data)[0])
    probability = float(model.predict_proba(input_data)[0][1])
    result = "Converted" if prediction == 1 else "Not Converted"
    return jsonify(
        {
            "prediction": result,
            "conversion_probability": round(probability, 3),
        }
    )


@app.post("/v1/predictBatch")
def predict_batch():
    file = request.files["file"]
    input_data = pd.read_csv(file)
    input_data = input_data[FEATURE_ORDER]
    predictions = model.predict(input_data)
    probabilities = model.predict_proba(input_data)[:, 1]
    results = [
        {
            "prediction": "Converted" if int(pred) == 1 else "Not Converted",
            "conversion_probability": round(float(prob), 3),
        }
        for pred, prob in zip(predictions, probabilities)
    ]
    return jsonify(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=7860, debug=True)
