#!/usr/bin/python3
"""API controllers for City."""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import State
from models.state import State
import json


@app_views.route("/states/<id_state>/cities", methods=["GET"])
def get_cities(id_state):
    """Get All City by State ID."""
    state = storage.get(State, id_state)
    city_list = []

    if state is None:
        abort(404)

    for city in state.cities:
        city_list.append(city.to_dict())

    response = make_response(json.dumps(city_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>", methods=["GET"])
def get_city(id):
    """Get City by ID."""
    city = storage.get(State, id)

    if city is None:
        abort(404)

    data = city.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>", methods=["DELETE"])
def delete_city(id):
    """Delete City by ID."""
    city = storage.get(State, id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    data = {}
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id_state>/cities", methods=["POST"])
def create_city(id_state):
    """Create City with valid state ID."""
    state = storage.get(State, id_state)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    body = request.get_json()
    city = State(**body)
    city.state_id = id_state
    city.save()

    data = city.to_dict()
    response = make_response(json.dumps(data), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>", methods=["PUT"])
def put_city(id):
    """Update City by ID."""
    city = storage.get(State, id)
    exclude_keys = ["id", "state_id", "created_at", "updated_at"]

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    body = request.get_json()
    for key, value in body.items():
        if key not in exclude_keys:
            setattr(city, key, value)
    storage.save()

    data = city.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response
