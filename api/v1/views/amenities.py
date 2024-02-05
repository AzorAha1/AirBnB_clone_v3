#!/usr/bin/python3
"""handles all the default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.amenity import Amenity
gt = ['GET']
dt = ['DELETE']


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def allamenity():
    """list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=gt, strict_slashes=False)
def getamenitybyid(amenity_id):
    """retrieve Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=dt, strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create amenity"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_amenity = Amenity(**data)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('amenities/<amenity_id>')
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(400, 'Not a Json')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif not amenity:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
