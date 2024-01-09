#!/usr/bin/python3
""" View for City objects that handles default API actions """
from flasgger.utils import swag_from
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/cities_by_state_get.yml', methods=['GET'])
def get_cities(state_id):
    """ Gets cities for state_id """
    state = storage.get(State, state_id)
    print(state)
    if state is None:
        abort(404)
    list_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/cities_get.yml', methods=['GET'])
def r_city_id(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/cities_del.yml', methods=['DELETE'])
def del_city(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/cities_post.yml', methods=['POST'])
def post_city(state_id):
    """ Creates a City object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if "name" not in new_city:
        abort(400, "Missing name")
    city = City(**new_city)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/cities_put.yml', methods=['PUT'])
def put_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
