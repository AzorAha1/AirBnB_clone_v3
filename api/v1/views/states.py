#!/usr/bin/python3
"""handles all the default RESTFul API actions"""

from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State
dm = ['DELETE']


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """retrieves the list of all states objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object using state_id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=dm, strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a state"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif not state:
        abort(404)

    for key, value in data.items():
        if key not in ['id', 'create_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
