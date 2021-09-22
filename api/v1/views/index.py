#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask.json import jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route('/status')
def status():
    return (jsonify({"status" : "OK"}))

@app_views.route('/stats')
def stats_db():
    finalDicto = {}
    for key, value in classes.items():
        finalDicto[key] = storage.count(value)
    return(jsonify(finalDicto))