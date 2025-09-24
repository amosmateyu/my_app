from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from .models import Patient_data
import pandas as pd
from .machine import generate_personalized_recommendations
from .connectors import db

patient_bp = Blueprint("patient", __name__)

@patient_bp.route("/recent_patient", methods=["GET"])
@login_required
def recent_patient():
    recent_patient = (
        Patient_data.query.filter_by(doctor_id=current_user.id)
        .order_by(Patient_data.id.desc())
        .first()
    )





    FEATURE_ORDER = [
    "high_blood_pressure",
    "high_cholesterol_level",
    "has_diabetes",
    "has_obesity",
    "sedentary_lifestyle",
    "family_history_of_heart_disease",
    "chronic_stress_level",
    "smoking_habit",
    "age_in_years",
    "gender_identity"
    ]

    # Example of converting a recent patient to DataFrame
    patient_data = {
    "high_blood_pressure": recent_patient.high_blood_pressure,
    "high_cholesterol_level": recent_patient.high_cholesterol_level,
    "has_diabetes": recent_patient.has_diabetes,
    "has_obesity": recent_patient.has_obesity,
    "sedentary_lifestyle": recent_patient.sedentary_lifestyle,
    "family_history_of_heart_disease": recent_patient.family_history_of_heart_disease,
    "chronic_stress_level": recent_patient.chronic_stress_level,
    "smoking_habit": recent_patient.smoking_habit,
    "age_in_years": recent_patient.age_in_years,
    "gender_identity": recent_patient.gender_identity
}

    # Convert to DataFrame keeping the order
    patient_df = pd.DataFrame([patient_data], columns=FEATURE_ORDER)
    
   
   
    recommendations = generate_personalized_recommendations(patient_df)
    # Update patient record
    prob_float = float(recommendations["probability"].replace('%', ''))
    recent_patient.heart_disease_risk_score = prob_float
    recent_patient.risk_level = recommendations["predicted_class"]
    db.session.commit()

   
   

    return jsonify({
        "riskDescription": "The above propabality your 10 year risk level.",
        "recommendationsIntro": "Based on your top risk factors, here are personalized recommendations:",
        "probability": recommendations["probability"],
        "risk_level": recommendations["predicted_class"],
        "recommendations": recommendations["recommendations"]
    })
