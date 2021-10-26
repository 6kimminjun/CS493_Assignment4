from flask import Blueprint, request
from google.cloud import datastore
import json
from json2html import *
import constants

client = datastore.Client()

bp = Blueprint('loads', __name__, url_prefix='/loads')

@bp.route('', methods=['POST','GET'])
def loads_get_post():
    if request.method == 'POST':
        content = request.get_json()
        new_loads = datastore.entity.Entity(key=client.key(constants.loads))
        new_loads.update({"name": content["name"]})
        client.put(new_loads)
        return str(new_loads.key.id)
    elif request.method == 'GET':
        query = client.query(kind=constants.loads)
        q_limit = int(request.args.get('limit', '2'))
        q_offset = int(request.args.get('offset', '0'))
        g_iterator = query.fetch(limit= q_limit, offset=q_offset)
        pages = g_iterator.pages
        results = list(next(pages))
        if g_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
        output = {"loads": results}
        if next_url:
            output["next"] = next_url
        return json.dumps(output)


@bp.route('/<id>', methods=['PUT','DELETE'])
def loads_put_delete(id):
    if request.method == 'PUT':
        content = request.get_json()
        loads_key = client.key(constants.loads, int(id))
        loads = client.get(key=loads_key)
        loads.update({"name": content["name"]})
        client.put(loads)
        return ('',200)
    elif request.method == 'DELETE':
        key = client.key(constants.loads, int(id))
        client.delete(key)
        return ('',200)
    else:
        return 'Method not recogonized'