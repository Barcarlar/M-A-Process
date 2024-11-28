import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key_here'

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To disable the Flask-SQLAlchemy event system

    # Flask-Mail configuration for sending emails
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.example.com'  # Example: Gmail or SendGrid SMTP server
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)  # Common port for TLS
    MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS') or True)
    MAIL_USE_SSL = bool(os.environ.get('MAIL_USE_SSL') or False)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  # Your email address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  # Your email password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your_email@example.com'

    # Optional settings for better debugging
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    DEBUG = os.environ.get('DEBUG') or True
