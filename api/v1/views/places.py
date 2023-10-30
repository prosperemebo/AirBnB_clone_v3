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


@app_views.route('/places_search', methods=['POST'])
def places_search_enhanced():
    """Search Place."""
    body = request.get_json()
    places_list = []

    if body is None:
        abort(400, description="Not a JSON")

    if body and len(body):
        states = body.get('states', None)
        cities = body.get('cities', None)
        amenities = body.get('amenities', None)

    if not body or not len(body) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        places_list = [place.to_dict() for place in places]

        response = make_response(json.dumps(places_list), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    if states:
        states_instance = [storage.get(State, s_id) for s_id in states]
        for state in states_instance:
            if state:
                for city in state.cities:
                    if city:
                        places_list.extend(place for place in city.places)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if places_list is None:
            places_list = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        places_list = [place for place in places_list
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for place in places_list:
        new_place = place.to_dict()
        new_place.pop('amenities', None)

        places.append(new_place)

    response = make_response(json.dumps(places), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
