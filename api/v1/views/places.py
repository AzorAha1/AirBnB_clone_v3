#!/usr/bin/python3
""" a new view for Place objects that handles all
default RESTFul API actions"""

from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from api.v1.views import app_views

gt = ['GET']
dt = ['DELETE']
pt = ['PUT']


@app_views.route('/cities/<city_id>/places', methods=gt, strict_slashes=False)
def get_all_places(city_id):
    """list of all Place objects ids"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=gt, strict_slashes=False)
def place_id(place_id):
    """retrieves Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=dt, strict_slashes=False)
def delete_place(place_id):
    """delete a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place():
    """create a new Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place:
        abort(400, 'Missing user_id')
    user_id = new_place['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in new_place:
        abort(400, 'Missing name')

    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=pt, strict_slashes=False)
def update_place(place_id):
    """update a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id',
                       'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
