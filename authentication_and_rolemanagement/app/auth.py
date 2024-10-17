from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, get_jwt
)
from app.models import User, db
from app.security import generate_captcha, verify_captcha

auth_blueprint = Blueprint('auth', __name__)

# User registration route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    captcha = data.get('captcha')
    actual_captcha = data.get('actual_captcha')

    if not verify_captcha(captcha, actual_captcha):
        return jsonify({"error": "Invalid CAPTCHA"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# Login route
@auth_blueprint.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"username": user.username, "role": user.role})
    refresh_token = create_refresh_token(identity={"username": user.username, "role": user.role})

    return jsonify(access_token=access_token, refresh_token=refresh_token), 200

# Logout route
@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200

# Token refresh route
@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify(access_token=access_token), 200
