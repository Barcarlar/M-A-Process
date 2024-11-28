from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Initialize database and bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

# User model
class User(UserMixin, db.Model):
    """
    Represents a user in the system, including authentication and role information.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')  # Default role is 'user'
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    
    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def check_password(self, password):
        """
        Verify the provided password against the stored hash.
        """
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        """
        Hash and set the password.
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @classmethod
    def get_by_email(cls, email):
        """
        Retrieve a user by email.
        """
        return cls.query.filter_by(email=email).first()

    def is_admin(self):
        """
        Check if the user has admin privileges.
        """
        return self.role == 'admin'

    def __repr__(self):
        return f"<User(username={self.username}, email={self.email})>"

# Post model
class Post(db.Model):
    """
    Represents a content post created by users.
    """
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self):
        return f"<Post(title={self.title}, date_posted={self.date_posted})>"

# Profile model
class Profile(db.Model):
    """
    Stores additional user information, like bio and avatar.
    """
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.String(500), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True, default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('profile', uselist=False, lazy=True))

    def __init__(self, bio=None, avatar_url='default.jpg', user_id=None):
        self.bio = bio
        self.avatar_url = avatar_url
        self.user_id = user_id

    def __repr__(self):
        return f"<Profile(user={self.user.username}, avatar_url={self.avatar_url})>"

# Role model
class Role(db.Model):
    """
    Represents roles for users, e.g., admin, user.
    """
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    users = db.relationship('User', secondary='user_roles', backref='roles')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Role(name={self.name})>"

# UserRoles association table
class UserRoles(db.Model):
    """
    Association table for many-to-many relationships between users and roles.
    """
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)

    user = db.relationship(User, backref=db.backref('user_roles', cascade='all, delete-orphan'))
    role = db.relationship(Role, backref=db.backref('user_roles', cascade='all, delete-orphan'))

# Function to initialize the database
def init_db():
    """
    Create all tables in the database.
    """
    with current_app.app_context():
        db.create_all()
