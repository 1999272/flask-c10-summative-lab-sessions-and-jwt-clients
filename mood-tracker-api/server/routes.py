from flask import request, session, jsonify

from app import app
from models import db, User



@app.post('/signup')
def signup():
    json_data = request.get_json(silent=True) or {}
    username = json_data.get('username')
    password = json_data.get('password')

    if not username or not password:
        return jsonify({"error": ["Username and password are required"]}), 400

    try:
        user = User(username=username)
        user.password_hash = password
        db.session.add(user)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({"error": [str(err)]}), 400

    session['user_id'] = user.id

    return jsonify({"id": user.id, "username": user.username}), 201