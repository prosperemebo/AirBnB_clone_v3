#!/usr/bin/python3
"""API Controllers for Amenities."""
from flask import abort, make_response
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
import json
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE")


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def get_place_amenities(place_id):
    """Get All Amenities by Place."""
    place = storage.get(Place, place_id)
    amenities_list = []

    if place is None:
        abort(404)

    if storage_type == "db":
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        for id in place.amenity_ids:
            amenity = storage.get(Amenity, id)
            amenities_list.append(amenity.to_dict())

    response = make_response(json.dumps(amenities_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity(place_id, amenity_id):
    """Delete Amenity."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)

    if amenity is None:
        abort(404)

    if storage_type == "db":
        if amenity not in place.amenities:
            abort(404)

        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)

        place.amenity_ids.remove(amenity_id)

    storage.save()

    response = make_response(json.dumps({}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=["POST"])
def create_place_amenity(place_id, amenity_id):
    """Link Amenity to Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None:
        abort(404)

    if amenity is None:
        abort(404)

    if storage_type == "db":
        if amenity in place.amenities:
            response = make_response(json.dumps(amenity.to_dict()), 200)
            response.headers["Content-Type"] = "application/json"
            return response

        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return amenity, 200

        place.amenity_ids.append(amenity_id)

    storage.save()

    response = make_response(json.dumps(amenity.to_dict()), 201)
    response.headers["Content-Type"] = "application/json"
    return response
