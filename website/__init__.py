from flask import Flask
from .connectors import db, login_manager, init_extensions
from .central_router import register_blueprints
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    # Initialize extensions and config
    init_extensions(app)
    
    migrate = Migrate(app, db)

    # Import models AFTER db is initialized
    from .models import Doctor_data, Patient_data

    @login_manager.user_loader
    def load_user(user_id):
        return Doctor_data.query.get(int(user_id))

    # Register all blueprints
    register_blueprints(app)

    # Drop and recreate tables (⚠️ wipes all data)
    #with app.app_context():
       # db.drop_all()
       # db.create_all()
        #print("✅ Database reset complete!")

    # Flask-Migrate will handle schema creation via `flask db upgrade`
    return app
