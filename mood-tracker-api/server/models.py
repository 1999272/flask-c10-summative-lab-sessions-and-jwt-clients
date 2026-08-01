from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    @property
    def password_hash(self):
        raise AttributeError("Password hashes may not be viewed.")

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode('utf-8'))
    @validates("username")
    def validate_username(self, key, value):
        if not value or not value.strip():
            raise ValueError("Username cannot be empty.")
        if len(value) > 50:
            raise ValueError("Username must be 50 characters or fewer.")
        return value.strip()


class MoodEntry(db.Model):
    __tablename__ = "mood_entries"

    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String, nullable=False)
    intensity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", backref="mood_entries")

    @validates("mood")
    def validate_mood(self, key, value):
        if not value or not value.strip():
            raise ValueError("Mood cannot be empty.")
        return value.strip()

    @validates("intensity")
    def validate_intensity(self, key, value):
        if value is None or not (1 <= value <= 10):
            raise ValueError("Intensity must be between 1 and 10.")
        return value
