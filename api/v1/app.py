#!/usr/bin/python3
""" Index """

from os import getenv
from flask import Flask
from flask.blueprints import Blueprint
from flask import jsonify, request


app = Flask(__name__)

from models import storage
from api.v1.views import app_views

app.register_blueprint(app_views)

app.config.update(
    JSONIFY_PRETTYPRINT_REGULAR=True
)

@app.errorhandler(404)
def not_found(e):
    return (jsonify({"error": "Not found"})), 404

@app.teardown_appcontext
def close_storage(exception):
    # Return close session on
    storage.close()


if __name__ == "__main__":
    try:
        app.run(
            host=getenv('HBNB_API_HOST'),
            port=getenv('HBNB_API_PORT')
            )
    except:
        app.run(host='0.0.0.0', port=5000, threaded=True)