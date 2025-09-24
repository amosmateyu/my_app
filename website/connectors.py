import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import sys

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  

def init_extensions(app):
    try:
        # Load configs
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
        app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_timeout": 30,
        "pool_recycle": 1800
            }


        if not app.config['SQLALCHEMY_DATABASE_URI']:
            raise ValueError("DATABASE_URL not found in environment variables!")

        # Initialize extensions
        db.init_app(app)
        login_manager.init_app(app)

        print(f"✅ Connected to database: {app.config['SQLALCHEMY_DATABASE_URI']}")

    except Exception as e:
        # Print error to console and stderr (Render logs will capture this)
        print(f"❌ Database initialization error: {e}", file=sys.stderr)
        # Optionally re-raise so Flask fails loudly
        raise
