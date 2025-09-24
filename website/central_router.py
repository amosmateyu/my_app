from .auth import auth_bp
from .views import main_bp
from .document_routes import report
from .prediction import prediction_bp
from .patient_routes import patient_bp

def register_blueprints(app):
    """Centralize blueprint registration."""
    #patient_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="/home")
    app.register_blueprint(report , url_prefix="/report")
    app.register_blueprint(prediction_bp, url_prefix="/predict")
    app.register_blueprint(patient_bp, url_prefix="/patient")
