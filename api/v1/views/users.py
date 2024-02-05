#!/usr/bin/python3
"""handles all the default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.user import User
gt = ['GET']
dt = ['DELETE']
pt = ['PUT']


@app_views.route('/users', methods=gt, strict_slashes=False)
def allusers():
    """list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=gt, strict_slashes=False)
def getuserbyid(user_id):
    """retrieve User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=dt, strict_slashes=False)
def delete_user(user_id):
    """delete user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create user"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'email' not in data:
        abort(400, 'Missing email')
    elif 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('users/<user_id>', methods=pt, strict_slashes=False)
def update_user(user_id):
    """update User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
