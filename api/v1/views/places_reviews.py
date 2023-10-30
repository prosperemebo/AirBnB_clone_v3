#!/usr/bin/python3
"""API Controller for Reviews."""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
import json


@app_views.route("/places/<id_place>/reviews", methods=["GET"])
def get_reviews(place_id):
    """Get All Reviews by Place."""
    place = storage.get(Place, place_id)
    reviews_list = []

    if place is None:
        abort(404)

    for review in place.reviews:
        reviews_list.append(review.to_dict())

    response = make_response(json.dumps(reviews_list), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<id>", methods=["GET"])
def get_review(review_id):
    """Get Reviews by ID."""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    data = review.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<id>", methods=["DELETE"])
def delete_review(review_id):
    """Delete Review by ID."""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    response = make_response(json.dumps({}), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/places/<id_place>/reviews", methods=["POST"])
def create_review(place_id):
    """Create Review."""
    place = storage.get(Place, place_id)
    body = request.get_json()

    if place is None:
        abort(404)

    if not body:
        abort(400, description='Not a JSON')

    if "user_id" not in body:
        abort(400, description="Missing user_id")

    if not storage.get(User, body.get("user_id")):
        abort(404)

    if "text" not in body:
        abort(400, description="Missing text")

    review = Review(**body)
    review.place_id = place_id
    review.save()

    data = review.to_dict()
    response = make_response(json.dumps(data), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/reviews/<id>", methods=["PUT"])
def put_review(review_id):
    """Update Review."""
    body = request.get_json()
    review = storage.get(Review, review_id)
    excluded_fields = ["id", "user_id", "place_id", "created_at", "updated_at"]

    if review is None:
        abort(404)

    if body is None:
        abort(400, description="Not a JSON")

    for field, value in body.items():
        if field not in excluded_fields:
            setattr(review, field, value)

    storage.save()

    data = review.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response
