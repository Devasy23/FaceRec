from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db

# Update user profile route
@auth_blueprint.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_user_data = get_jwt_identity()
    data = request.json

    user = User.query.filter_by(username=current_user_data['username']).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    user.username = data.get('username', user.username)
    
    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"}), 200
