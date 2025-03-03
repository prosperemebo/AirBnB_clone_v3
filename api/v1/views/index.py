#!/usr/bin/python3
"""API root enspoint."""
import json

from flask import make_response
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Handle API status."""
    data = {"status": "OK"}
    response = make_response(json.dumps(data), 200)
    response.headers['Content-Type'] = 'application/json'
    return response


@app_views.route("/stats")
def stats():
    """Handle API stats."""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User

    data = {
        "amenities": storage.count(Amenity),
        "cities":  storage.count(City),
        "places":  storage.count(Place),
        "reviews":  storage.count(Review),
        "states":  storage.count(State),
        "users":  storage.count(User)
    }
    response = make_response(json.dumps(data), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
