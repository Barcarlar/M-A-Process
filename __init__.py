from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configurations
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Login manager settings
    login_manager.login_view = 'auth.login'  # Replace with your login route name
    login_manager.login_message_category = 'info'

    # Register blueprints
    from yourapplication.auth.routes import auth
    from yourapplication.main.routes import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
