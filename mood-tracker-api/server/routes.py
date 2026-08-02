from flask import request, session, jsonify
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, User, MoodEntry



@app.post('/signup')
def signup():
    json_data = request.get_json(silent=True) or {}
    username = json_data.get('username')
    password = json_data.get('password')

    if not username or not password:
        return jsonify({"errors": ["Username and password are required."]}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"errors": ["Username is already taken."]}), 400

    try:
        user = User(username=username)
        user.password_hash = password
        db.session.add(user)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"errors": ["Username is already taken."]}), 400

    session['user_id'] = user.id

    return jsonify({"id": user.id, "username": user.username}), 201


@app.post('/login')
def login():
    json_data = request.get_json(silent=True) or {}
    username = json_data.get('username')
    password = json_data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        session['user_id'] = user.id
        return jsonify({"id": user.id, "username": user.username}), 200

    return jsonify({"errors": ["Invalid username or password."]}), 401


@app.get('/check_session')
def check_session():
    user_id = session.get('user_id')

    if user_id:
        user = db.session.get(User, user_id)
        if user:
            return jsonify({"id": user.id, "username": user.username}), 200

    return jsonify({"errors": ["Unauthorized"]}), 401


@app.delete('/logout')
def logout():
    session['user_id'] = None
    return {}, 204   


@app.get('/mood_entries')
def get_mood_entries():
    if not session.get('user_id'):
        return jsonify({"errors": ["Unauthorized"]}), 401

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = MoodEntry.query.filter_by(
        user_id=session['user_id']
    ).paginate(page=page, per_page=per_page, error_out=False)

    entries = [
        {
            "id": e.id,
            "mood": e.mood,
            "intensity": e.intensity,
            "note": e.note,
            "created_at": e.created_at.isoformat() if e.created_at else None,
            "user_id": e.user_id,
        }
        for e in pagination.items
    ]

    return jsonify({
        "entries": entries,
        "page": pagination.page,
        "total_pages": pagination.pages,
        "total_entries": pagination.total,
    }), 200


@app.post('/mood_entries')
def create_mood_entry():
    if not session.get('user_id'):
        return jsonify({"errors": ["Unauthorized"]}), 401

    json_data = request.get_json(silent=True) or {}

    try:
        entry =MoodEntry(
            mood=json_data.get('mood'),
            intensity=json_data.get('intensity'),
            note=json_data.get('note'),
            user_id=session['user_id']
        )
        db.session.add(entry)
        db.session.commit()
    except (ValueError, IntegrityError) as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400

    return jsonify({
        "id": entry.id,
        "mood": entry.mood,
        "intensity": entry.intensity,
        "note": entry.note,
        "created_at": entry.created_at.isoformat() if entry.created_at else None,
        "user_id": entry.user_id,
    }), 201

def find_owned_entry(id):
    entry = db.session.get(MoodEntry, id)

    if not entry:
        return None, (jsonify({"errors": ["Mood entry not found."]}), 404)

    if entry.user_id != session['user_id']:
        return None, (jsonify({"errors": ["Forbidden."]}), 403)

    return entry, None