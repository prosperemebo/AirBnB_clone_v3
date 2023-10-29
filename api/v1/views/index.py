#!/usr/bin/python3
"""API root enspoint."""
import json

from flask import make_response
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Handle API status."""
    res = {"status": "OK"}
    response = make_response(json.dumps(res), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
