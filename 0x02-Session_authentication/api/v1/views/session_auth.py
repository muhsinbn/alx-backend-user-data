#!/usr/bin/env python3
""" Module that handles all routes for session Auth
"""
from flask import Blueprint, jsonify, abort, request
from models.user import User
from api.v1.auth.session_auth import SessionAuth
from api.v1.views import app_views
import os


@app_views.route(
            '/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles the login process for session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400

    if not password or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Handles the logout process for session authentication
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
