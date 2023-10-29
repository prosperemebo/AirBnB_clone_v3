#!/usr/bin/python3
"""API controllers for State."""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
import json


@app_views.route("/states", methods=["GET"])
def get_states():
    """Get all States."""
    states = storage.all(State).values()
    states_list = []

    for state in states:
        states_list.append(state.to_dict())

    response = make_response(json.dumps(states_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id>", methods=["GET"])
def get_state(id):
    """Get State by ID."""
    state = storage.get(State, id)

    if state is None:
        abort(404)

    data = state.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id>", methods=["DELETE"])
def delete_state(id):
    """Delete state by ID."""
    state = storage.get(State, id)

    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states", methods=["POST"])
def create_state():
    """Create State."""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    state = State(**data)
    state.save()

    res = state.to_dict()
    response = make_response(json.dumps(res), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/states/<id>", methods=["PUT"])
def put_state(id):
    """Update State."""
    state = storage.get(State, id)
    exclude_keys = ["id", "created_at", "updated_at"]

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in exclude_keys:
            setattr(state, key, value)
    storage.save()

    res = state.to_dict()
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response
