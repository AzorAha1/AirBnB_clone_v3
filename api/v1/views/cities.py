#!/usr/bin/python3
"""handles all the default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request
from models.city import City
from models.state import State
gt = ['GET']
pt = ['POST']


@app_views.route('/states/<state_id>/cities', methods=gt, strict_slashes=False)
def getallcity(state_id):
    """get all cities"""
    cities = storage.all(City).values()
    # filter cities that match the state id
    correctcities = [city for city in cities if city.state_id == state_id]
    if not correctcities:
        abort(404)
    return jsonify([city.to_dict() for city in correctcities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def getcitybyid(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def deletecity(city_id):
    """delete city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    elif city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=pt, strict_slashes=False)
def create_city(state_id):
    """create city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif state is None:
        abort(404)
    thedata = request.get_json()
    if not thedata:
        abort(400, 'Not a JSON')
    if 'name' not in thedata:
        abort(400, 'Missing name')
    # thenewcity = City(name=thedata['name'], state_id=state_id)
    # storage.new(thenewcity)
    # storage.save()
    thedata['state_id'] = state_id
    city = City(**thedata)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updatecity(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    thedata = request.get_json()
    if not thedata:
        abort(400, 'Not a JSON')
    elif city is None:
        abort(404)
    for key, value in thedata.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
