#!/usr/bin/python3
"""AirBnB v3 flask API v1."""
from flask import Flask, make_response
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv
from dotenv import load_dotenv
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

load_dotenv()

host = getenv("HBNB_API_HOST")
port = getenv("HBNB_API_PORT")

cors = CORS(
    app,
    resources={r"/*": {"origins": "0.0.0.0"}}
)


@app.teardown_appcontext
def teardown(err):
    """Close API storage."""
    from models import storage

    storage.close()


@app.errorhandler(404)
def not_found(err):
    """Handle 404."""
    res = {'error': "Not found"}
    response = make_response(json.dumps(res), 404)
    response.headers['Content-Type'] = 'application/json'

    return response


if __name__ == "__main__":
    """Application entry point."""
    host = "0.0.0.0" if host is None else host
    port = "5000" if port is None else port
    app.run(host=host, port=port, threaded=True)
