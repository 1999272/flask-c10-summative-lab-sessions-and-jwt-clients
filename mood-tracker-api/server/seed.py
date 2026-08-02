import random
from faker import Faker

from app import app
from models import db, User, MoodEntry

fake = Faker()

MOODS = ["happy", "sad", "anxious", "calm", "excited", "tired", "angry", "grateful"]