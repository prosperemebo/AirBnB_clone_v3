#!/usr/bin/python3
"""API Controller for User."""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route("/users", methods=["GET"])
def get_users():
    """Get All Users."""
    allUsers = storage.all(User).values()
    usersList = []
    for user in allUsers:
        usersList.append(user.to_dict())
    response = make_response(json.dumps(usersList), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["GET"])
def get_user(id):
    """Get User by ID."""
    user = storage.get(User, id)
    if not user:
        abort(404)
    response_data = user.to_dict()
    response = make_response(json.dumps(response_data), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    """Delete User."""
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    res = {}
    response = make_response(json.dumps(res), 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users", methods=["POST"])
def create_user():
    """Create new User."""
    body = request.get_json()

    if body is None:
        abort(400, description="Not a JSON")

    if "email" not in body:
        abort(400, description="Missing email")

    if "password" not in body:
        abort(400, description="Missing password")

    user = User(**body)
    user.save()

    data = user.to_dict()
    response = make_response(json.dumps(data), 201)
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/users/<id>", methods=["PUT"])
def put_user(id):
    """Update User."""
    body = request.get_json()
    user = storage.get(User, id)
    exclude_fields = ["id", "email", "created_at", "updated_at"]

    if user is None:
        abort(404)

    if body is None:
        abort(400, description="Not a JSON")

    for key, value in body.items():
        if key not in exclude_fields:
            setattr(user, key, value)

    storage.save()

    data = user.to_dict()
    response = make_response(json.dumps(data), 200)
    response.headers["Content-Type"] = "application/json"
    return response
