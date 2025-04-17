from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
import os
from datetime import timedelta

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:202120020@localhost:5432/forensics'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_PERMANENT'] = False
    app.permanent_session_lifetime = timedelta(minutes=120)

    # Flask-Mail config
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'stegoforensics@gmail.com'
    app.config['MAIL_PASSWORD'] = 'cnktiwvmhmtrwppd'

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import parts of our application
        from . import routes, models, embedding, crypto

        # Create database tables
        db.create_all()

    return app