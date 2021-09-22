#!/usr/bin/python3
""" State methods """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.engine.db_storage import classes


@app_views.route('/states/', methods=['GET', 'POST'])
def states_methods():
    if request.method == 'POST':
        storage.reload()
        jsonDicto = request.get_json()
        if jsonDicto is None:
            abort(400, 'Not a JSON')
        if "name" not in jsonDicto:
            abort(400, 'Missing name')
        newState = classes['State'](**jsonDicto)
        storage.new(newState)
        storage.save()
        storage.reload()
        return jsonify(
                storage.get(newState.__class__, newState.id).to_dict()), 201
                
    else:
        listDicto = []
        dicto = storage.all(classes['State'])
        for str, obj in dicto.items():
            objDicto = {}
            for key, value in obj.to_dict().items():
                objDicto[key] = value
            listDicto.append(objDicto)
        return jsonify(listDicto)


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def states_id_methods(state_id):
    totalDicto = storage.all()
    copyTypeClass = {}
    status = 0

    # Main iterator: get obj based on unique id, if not, status=0 == abort(404)
    for key, value in totalDicto.items():
        typeClass = key.split(".")
        if typeClass[1] == str(state_id) and typeClass[0] == "State":
            status = 1
            copyTypeClass[str(typeClass)] = value
            break

    if request.method == 'PUT':
        print("oki doki")
        if status == 0:
            abort(404)
        else:
            jsonDicto = request.get_json()
            if jsonDicto is None:
                abort(400, 'Not a JSON')
            for key, value in copyTypeClass.items():
                for usrKey, usrValue in jsonDicto.items():
                    if usrKey == "id" or\
                        usrKey == "created_at" or usrKey == "updated_at":
                        pass
                    setattr(value, usrKey, usrValue)
                storage.new(value)
                storage.save()
                storage.reload()
                return jsonify(value.to_dict()), 200
            

    elif request.method == 'DELETE':
        try:
            if status == 0:
                abort(404)
            else:
                for key, value in copyTypeClass.items():
                    storage.delete(value)
                    storage.save()
                    storage.reload()
                    return jsonify(), 200
        except:
            abort(404)
    else:
        if status == 0:
            abort(404)
        else:
            for key, value in copyTypeClass.items():
                return(jsonify(value.to_dict()))
