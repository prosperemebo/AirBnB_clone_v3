#!/usr/bin/python3
"""API Controllers for Place Model."""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
import json


@app_views.route("/cities/<id>/places", methods=["GET"])
def get_places(id):
    """Get All Places by ID."""
    city = storage.get(City, id)
    city_places = []

    if city is None:
        abort(404)

    for place in city.places:
        city_places.append(place.to_dict())

    data = city_places
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<id>", methods=["GET"])
def get_place(id):
    """Get Place by ID."""
    place = storage.get(Place, id)

    if place is None:
        abort(404)

    data = place.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<id>", methods=["DELETE"])
def delete_place(id):
    """Delete Place."""
    place = storage.get(Place, id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    response = make_response(json.dumps({}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/cities/<id>/places", methods=["POST"])
def post_place(id):
    """Create Place."""
    city = storage.get(City, id)
    body = request.get_json()

    if city is None:
        abort(404)

    if not body:
        abort(400, description="Not a JSON")

    if "user_id" not in body:
        abort(400, description="Missing user_id")

    user = storage.get(User, body["user_id"])

    if user is None:
        abort(404)

    if "name" not in body:
        abort(400, description="Missing name")

    body["city_id"] = id
    place = Place(**body)
    place.save()

    data = place.to_dict()
    response = make_response(json.dumps(data), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<place_id>", methods=["PUT"])
def put_place(place_id):
    """Update Place."""
    place = storage.get(Place, place_id)
    body = request.get_json()
    excluded_fields = ["id", "user_id", "city_id", "created_at", "updated_at"]

    if place is None:
        abort(404)

    if body is None:
        abort(400, description="Not a JSON")

    for field, value in body.items():
        if field not in excluded_fields:
            setattr(place, field, value)

    storage.save()

    data = place.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response
