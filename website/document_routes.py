from flask import Blueprint, make_response, request, jsonify
from flask_login import current_user, login_required
from fpdf import FPDF
from .machine import generate_personalized_recommendations
from .models import Patient_data
import traceback
import pandas as pd
import io
from datetime import datetime
import os

# Paths
logo_path = os.path.join("website", "static", "images", "arm.png")
signature_path = os.path.join("website", "static", "images", "signature.png")

report = Blueprint("report", __name__)

# Define colors
colors = {
    "light_sage": (180, 184, 171),
    "dark_blue": (21, 50, 67),
    "medium_blue": (40, 75, 99),
    "light_cream": (244, 249, 233),
    "off_white": (238, 240, 235),
    "accent_gold": (138, 122, 106),
    "text_dark": (21, 50, 67),
    "text_light": (91, 94, 90)
}

# Correct FEATURE_ORDER
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



def generate_medical_report(patient_df, patient_details):
    # Step 1: Generate raw recommendations from the model
    recommendations = generate_personalized_recommendations(patient_df)

    # Step 2: Map internal feature names to human-readable labels
    feature_label_map = {
        "high_blood_pressure": "Blood Pressure",
        "high_cholesterol_level": "Cholesterol Level",
        "has_diabetes": "Diabetes Status",
        "has_obesity": "Obesity",
        "sedentary_lifestyle": "Activity Level",
        "family_history_of_heart_disease": "Family History of Heart Disease",
        "chronic_stress_level": "Stress Level",
        "smoking_habit": "Smoking Habit",
        "age_in_years": "Age",
        "gender_identity": "Gender"
    }

    # Pre-process recommendations to readable labels
    readable_recommendations = {}
    for feature, advice in recommendations.get("recommendations", {}).items():
        readable_feature = feature_label_map.get(feature, feature.replace("_", " ").title())
        readable_recommendations[readable_feature] = advice

    # ===== PDF Setup =====
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    effective_width = pdf.w - pdf.l_margin - pdf.r_margin

    # ===== Hospital Logo =====
    logo_width = 25
    x_center = (pdf.w - logo_width) / 2
    pdf.image(logo_path, x=x_center, y=10, w=logo_width)
    pdf.set_y(10 + logo_width + 8)

    # ===== Headers =====
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(*colors["dark_blue"])
    pdf.multi_cell(effective_width, 10, " The Ministry Of Health", align="C")
    pdf.ln(4)

    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(effective_width, 10, "Official Heart Risk Assessment Report", align="C")
    pdf.ln(10)

    # ===== Patient Details =====
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(*colors["medium_blue"])
    pdf.set_text_color(*colors["off_white"])
    pdf.multi_cell(effective_width, 8, "Patient Details", border=0, fill=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*colors["text_dark"])
    col1_width = effective_width * 0.6
    col2_width = effective_width * 0.4
    for key, value in patient_details.items():
        pdf.cell(col1_width, 7, f"{key}", border=0)
        pdf.cell(col2_width, 7, f"{value}", border=0, ln=1)
    pdf.ln(6)

    # ===== Heart Risk Results =====
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(*colors["medium_blue"])
    pdf.set_text_color(*colors["off_white"])
    pdf.multi_cell(effective_width, 8, "Heart Risk Results", border=0, fill=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*colors["text_dark"])
    for key, value in recommendations.items():
        if key == "recommendations":  # skip the internal key
            continue
        pdf.cell(col1_width, 7, f"{key}", border=0)
        pdf.cell(col2_width, 7, f"{value}", border=0, ln=1)
    pdf.ln(6)

    # ===== Recommendations =====
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(*colors["medium_blue"])
    pdf.set_text_color(*colors["off_white"])
    pdf.multi_cell(effective_width, 8, "Recommendations", border=0, fill=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*colors["text_dark"])
    for feature, advice in readable_recommendations.items():
        pdf.multi_cell(effective_width, 6, f"- {feature}: {advice}", align="L")
        pdf.ln(1)
    pdf.ln(4)

    # ===== Conclusion =====
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(*colors["medium_blue"])
    pdf.set_text_color(*colors["off_white"])
    pdf.multi_cell(effective_width, 8, "Conclusion", border=0, fill=True)
    pdf.ln(3)  # spacing after header

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(*colors["text_dark"])
    conclusion_text = (
        "Please follow all the above recommendations carefully. "
        "If your risk level is high, it is strongly advised to visit a cardiologist "
        "for further evaluation and guidance."
    )
    pdf.multi_cell(effective_width, 6, conclusion_text, align="L")
    pdf.ln(5)

    # ===== HSA Signature =====
    signature_width = 28
    x_center_sig = (pdf.w - signature_width) / 2
    y_position_sig = pdf.get_y() + 10
    pdf.image(signature_path, x=x_center_sig, y=y_position_sig, w=signature_width)

    pdf.set_y(y_position_sig + signature_width + 10)
    pdf.set_font("Arial", "I", 12)
    pdf.set_text_color(*colors["text_dark"])
    pdf.multi_cell(effective_width, 6, "HSA's Signature", align="C")
    pdf.ln(10)

    # ===== Footer =====
    pdf.set_y(pdf.get_y() + 5)
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(*colors["text_dark"])
    pdf.multi_cell(
        effective_width, 6,
        "Note: This report is generated based on the provided health data and is for informational purposes only.",
        align="L"
    )

    # Output PDF to memory buffer
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer



























@report.route("/download_report", methods=["GET"])
@login_required
def download_report():
    recent_patient = (
        Patient_data.query.filter_by(doctor_id=current_user.id)
        .order_by(Patient_data.id.desc())
        .first()
    )

    if not recent_patient:
        return jsonify({"error": "No patient found"}), 404

    # Build patient dictionary in FEATURE_ORDER
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

    # Reorder according to FEATURE_ORDER
    ordered_patient_data = {key: patient_data[key] for key in FEATURE_ORDER}

    # Convert to DataFrame for LIME/model
    patient_df = pd.DataFrame([ordered_patient_data])

    patient_details = {
        "First Name": recent_patient.first_name,
        "Last Name": recent_patient.last_name,
        "Date Issued": datetime.now().strftime("%d/%m/%Y")
    }

    pdf_buffer = generate_medical_report(patient_df, patient_details)
    response = make_response(pdf_buffer.getvalue())
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='medical_report.pdf')
    response.headers.set('Cache-Control', 'no-store')
    response.headers.set('X-Content-Type-Options', 'nosniff')
    return response


@report.route("/download_excel", methods=["GET"])
@login_required
def download_excel():
    try:
        patients = Patient_data.query.filter_by(doctor_id=current_user.id).all()
        data = []

        for p in patients:
            data.append({
                "First Name": p.first_name,
                "Last Name": p.last_name,
                "Age": p.age_in_years,
                "Gender": "Male" if p.gender_identity == 1 else "Female",
                "High Blood Pressure": "Yes" if p.high_blood_pressure == 1 else "No",
                "High Cholesterol": "Yes" if p.high_cholesterol_level == 1 else "No",
                "Diabetes": "Yes" if p.has_diabetes == 1 else "No",
                "Obesity": "Yes" if p.has_obesity == 1 else "No",
                "Sedentary Lifestyle": "Yes" if p.sedentary_lifestyle == 1 else "No",
                "Family History of Heart Disease": "Yes" if p.family_history_of_heart_disease == 1 else "No",
                "Chronic Stress": "Yes" if p.chronic_stress_level == 1 else "No",
                "Smoking Habit": "Yes" if p.smoking_habit == 1 else "No",
                "Risk Probability": p.heart_disease_risk_score,
                "Risk Level": p.risk_level,
            })

        df = pd.DataFrame(data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Patients")
        output.seek(0)

        response = make_response(output.getvalue())
        response.headers.set(
            'Content-Type',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response.headers.set(
            'Content-Disposition', 'attachment', filename='patients_data.xlsx'
        )
        response.headers.set('Cache-Control', 'no-store')
        response.headers.set('X-Content-Type-Options', 'nosniff')
        return response

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"status": "error", "message": str(e)}), 500
