#!/usr/bin/env python3
"""
flask view that handles all routes for session authentication
"""
from flask import jsonify, request
from api.v1.views import app_views
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session():
    """
    creates a session id for user id
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if user_email is None or len(user_email) == 0:
        return jsonify({"error": "email missing"}), 400
    if user_password is None or len(user_password) == 0:
        return jsonify({"error": "password missing"}), 400

    try:
        user_data = User.search({"email": user_email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_data:
        return jsonify({"error": "no user found for this email"}), 404

    for u in user_data:
        if not u.is_valid_password(user_password):
            return jsonify({"error": "wrong password"}), 401

    user = user_data[0]
    from api.v1.app import auth

    cookie = os.getenv("SESSION_NAME")
    session = auth.create_session(user.id)
    result = jsonify(user.to_json())
    result.set_cookie(cookie, session)
    return result
