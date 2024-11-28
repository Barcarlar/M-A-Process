from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate

# Initialize the Flask app
app = Flask(__name__)

# Secret key for session management
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and login manager
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Set the login view

# User model for storing user info in the database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Added email field
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Added role field with default value

# Login manager user loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']  # Use 'email' to match the form field
        password = request.form['password']

        try:
            user = User.query.filter_by(email=email).first()  # Query by email
            if user and check_password_hash(user.password, password):  # Check hashed password
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password. Please try again.', 'danger')
        except Exception as e:
            flash(f'Error during login: {str(e)}', 'danger')
    
    return render_template('login.html')

# Register page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']  # Added email field
        password = request.form['password']

        try:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists. Please choose another one.', 'danger')
            else:
                # Hash the password before saving
                hashed_password = generate_password_hash(password, method='sha256')
                new_user = User(username=username, email=email, password=hashed_password)  # Include email
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()  # Ensure rollback if there's an error during commit
            flash(f'Error during registration: {str(e)}', 'danger')

    return render_template('register.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        flash('You have been logged out.', 'info')
    except Exception as e:
        flash(f'Error during logout: {str(e)}', 'danger')
    
    return redirect(url_for('home'))

# Error handling for 404 and 500 errors
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

# Create the database tables if they don't exist
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f'Error creating database tables: {str(e)}')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
