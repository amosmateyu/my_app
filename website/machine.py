from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import joblib
import lime
import lime.lime_tabular
import os

# ===============================
# 1️⃣ Flask app setup
# ===============================


# ===============================
# 2️⃣ Load model and training data using environment variables
# ===============================
MODEL_FILE = os.environ.get("MODEL_FILE", "heart_risk_model.joblib")
DATA_FILE = os.environ.get("DATA_FILE", "training_data_sample.csv")

# Load model and training data
try:
    model = joblib.load(MODEL_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Model file not found: {MODEL_FILE}. Make sure it is uploaded and environment variable is set correctly."
    )

try:
    training_data = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    raise FileNotFoundError(
        f"Training data file not found: {DATA_FILE}. Make sure it is uploaded and environment variable is set correctly."
    )

feature_names = training_data.columns.tolist()
class_names = ["No Risk", "Risk"]

# ===============================
# 3️⃣ Initialize LIME Explainer
# ===============================
explainer = lime.lime_tabular.LimeTabularExplainer(
    training_data=training_data.values,
    feature_names=feature_names,
    class_names=class_names,
    mode='classification',
    random_state=42
)

# ===============================
# 4️⃣ Advice dictionaries
# ===============================
risk_advice = {
    "high_blood_pressure": "Maintain healthy blood pressure with low-salt diet and regular exercise.",
    "high_cholesterol_level": "Reduce cholesterol by avoiding fried foods and include healthy fats.",
    "has_diabetes": "Manage blood sugar through diet, exercise, and medications.",
    "has_obesity": "Maintain healthy weight through balanced diet and activity.",
    "sedentary_lifestyle": "Increase daily activity; aim for at least 30 minutes per day.",
    "family_history_of_heart_disease": "Regular check-ups and monitor risk factors closely.",
    "chronic_stress_level": "Practice stress management techniques like meditation or yoga.",
    "smoking_habit": "Quit smoking to reduce heart disease risk.",
    "age_in_years": "Regular health checkups are recommended due to age-related risk.",
    "gender_identity": "Follow general heart-healthy lifestyle recommendations."
}

positive_advice = {
    "high_blood_pressure": "Blood pressure looks good. Keep maintaining a healthy lifestyle!",
    "high_cholesterol_level": "Cholesterol level is within healthy range. Continue healthy eating.",
    "has_diabetes": "Blood sugar appears well-managed. Keep monitoring regularly.",
    "has_obesity": "Weight is in a healthy range. Maintain activity and diet.",
    "sedentary_lifestyle": "You are active enough. Keep up the good work!",
    "family_history_of_heart_disease": "No strong risk factor from family history. Keep healthy habits.",
    "chronic_stress_level": "Stress levels are manageable. Maintain relaxation routines.",
    "smoking_habit": "No smoking habit detected. Great for heart health!",
    "age_in_years": "Age factor is fine. Continue regular checkups.",
    "gender_identity": "Keep following heart-healthy lifestyle advice."
}

# ===============================
# 5️⃣ Wrapper for model + LIME
# ===============================
def predict_proba_wrapper(x_numpy):
    x_df = pd.DataFrame(x_numpy, columns=feature_names)
    return model.predict_proba(x_df)

def clean_feature_name(feature_label: str) -> str:
    return feature_label.split()[0]

def generate_personalized_recommendations(patient_df: pd.DataFrame):
    probs = predict_proba_wrapper(patient_df.values)[0]
    predicted_class = np.argmax(probs)
    is_high_risk = predicted_class == 1

    exp = explainer.explain_instance(
        patient_df.values[0],
        predict_proba_wrapper
    )

    lime_features = exp.as_list()
    recommendations = {}

    for feature_condition, contribution in lime_features:
        feature = clean_feature_name(feature_condition)
        if is_high_risk:
            advice = risk_advice.get(feature) if contribution > 0 else positive_advice.get(feature)
        else:
            advice = positive_advice.get(feature) if contribution < 0 else risk_advice.get(feature)
        if advice and feature not in recommendations:
            recommendations[feature] = advice

    return {
        "predicted_class": "High Risk" if is_high_risk else "Low Risk",
        "probability": f"{probs[predicted_class]*100:.2f}%",
        "recommendations": recommendations
    }
