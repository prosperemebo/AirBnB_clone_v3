#!/usr/bin/python3
"""API controlller for Amenities."""
from flask import abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
import json


@app_views.route("/amenities", methods=["GET"])
def get_amenities():
    """Get all amenities."""
    amenities = storage.all(Amenity).values()
    amenity_list = []

    for amenity in amenities:
        amenity_list.append(amenity.to_dict())

    response = make_response(json.dumps(amenity_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<id>", methods=["GET"])
def get_amenity(id):
    """Get amenity by ID."""
    amenity = storage.get(Amenity, id)

    if amenity is None:
        abort(404)

    data = amenity.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<id>", methods=["DELETE"])
def delete_amenity(id):
    """Delete amenity by ID."""
    amenity = storage.get(Amenity, id)

    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    response = make_response(json.dumps({}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities", methods=["POST"])
def create_amenity():
    """Create new Amenity."""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    body = request.get_json()
    amenity = Amenity(**body)
    amenity.save()

    data = amenity.to_dict()
    response = make_response(json.dumps(data), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<id>", methods=["PUT"])
def put_amenity(id):
    """Update Amenity."""
    amenity = storage.get(Amenity, id)
    exclude_keys = ["id", "created_at", "updated_at"]
    body = request.get_json()

    if amenity is None:
        abort(404)

    if body is None:
        abort(400, description="Not a JSON")

    for field, value in body.items():
        if field not in exclude_keys:
            setattr(amenity, field, value)

    storage.save()

    data = amenity.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response
