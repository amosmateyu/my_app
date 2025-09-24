from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Patient_data
from .connectors import db

prediction_bp = Blueprint("prediction", __name__)

@prediction_bp.route("/result", methods=["POST"])
@login_required
def result():
   
    if not current_user.is_authenticated:
        return jsonify({"status": "error", "message": "You must be logged in to submit health data."}), 401

    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received."}), 400

    try:
        # Extract values from frontend (should now match FEATURES_SAFE)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        age_in_years = data.get("age_in_years")
        gender_identity = data.get("gender_identity")
        high_blood_pressure = data.get("high_blood_pressure")
        high_cholesterol_level = data.get("high_cholesterol_level")
        has_diabetes = data.get("has_diabetes")
        has_obesity = data.get("has_obesity")
        sedentary_lifestyle = data.get("sedentary_lifestyle")
        family_history_of_heart_disease = data.get("family_history_of_heart_disease")
        chronic_stress_level = data.get("chronic_stress_level")
        smoking_habit = data.get("smoking_habit")

        # Save patient linked to current doctor
        new_patient = Patient_data(
            first_name=first_name,
            last_name=last_name,
            age_in_years=age_in_years,
            gender_identity=gender_identity,
            high_blood_pressure=high_blood_pressure,
            high_cholesterol_level=high_cholesterol_level,
            has_diabetes=has_diabetes,
            has_obesity=has_obesity,
            sedentary_lifestyle=sedentary_lifestyle,
            family_history_of_heart_disease=family_history_of_heart_disease,
            chronic_stress_level=chronic_stress_level,
            smoking_habit=smoking_habit,
            doctor_id=current_user.id
        )

        db.session.add(new_patient)
        db.session.commit()

        # Respond with success for JS to redirect
        return jsonify({"status": "success", "message": "Health data sent successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Failed to save data: {str(e)}"}), 500
