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

    print("Creating users...")
    users = []
    for _ in range(4):
        user = User(username=fake.unique.user_name())
        user.password_hash = "password123"
        users.append(user)
        db.session.add(user)
    db.session.commit()

    print("Creating mood entries...")
    for user in users:
        for _ in range(random.randint(3, 6)):
            entry = MoodEntry(
                mood=random.choice(MOODS),
                intensity=random.randint(1, 10),
                note=fake.sentence(),
                user=user,
            )
            db.session.add(entry)
    db.session.commit()

    print(f"Done — created {len(users)} users.")


if __name__ == "__main__":
    with app.app_context():
        seed_data()