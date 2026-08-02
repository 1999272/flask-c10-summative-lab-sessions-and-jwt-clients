import random
from faker import Faker

from app import app
from models import db, User, MoodEntry

fake = Faker()

MOODS = ["happy", "sad", "anxious", "calm", "excited", "tired", "angry", "grateful"]

def seed_data():
    print("Clearing old data...")
    MoodEntry.query.delete()
    User.query.delete()
    db.session.commit()