from flask import request, session, jsonify
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, User



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