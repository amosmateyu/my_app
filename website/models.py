from flask_login import UserMixin
from .connectors import db

class Doctor_data(UserMixin, db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)

    # ✅ Indexed for faster login queries
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(150), nullable=False)

    # Relationship to patients
    patients = db.relationship("Patient_data", backref="doctor", lazy=True)


class Patient_data(db.Model):
    __tablename__ = "patients"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)

    high_blood_pressure = db.Column(db.Integer, default=0)
    high_cholesterol_level = db.Column(db.Integer, default=0)
    has_diabetes = db.Column(db.Integer, default=0)
    has_obesity = db.Column(db.Integer, default=0)
    sedentary_lifestyle = db.Column(db.Integer, default=0)
    family_history_of_heart_disease = db.Column(db.Integer, default=0)
    chronic_stress_level = db.Column(db.Integer, default=0)
    smoking_habit = db.Column(db.Integer, default=0)
    age_in_years = db.Column(db.Integer)
    gender_identity = db.Column(db.Integer)  # 1 = Male, 0 = Female

    heart_disease_risk_score = db.Column(db.Float)
    risk_level = db.Column(db.String(50), nullable=True)  

    # ✅ Indexed foreign key for faster patient lookups by doctor
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False, index=True)
