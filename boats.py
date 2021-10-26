from flask import Blueprint, request
from google.cloud import datastore
import json
import constants

client = datastore.Client()

bp = Blueprint('boats', __name__, url_prefix='/boats')

@bp.route('', methods=['POST','GET'])
def boats_get_post():
    if request.method == 'POST':
        content = request.get_json()
        new_boats = datastore.entity.Entity(key=client.key(constants.boats))
        new_boats.update({'name': content['name'], 'description': content['description'],
          'price': content['price']})
        client.put(new_boats)
        return str(new_boats.key.id)
    elif request.method == 'GET':
        query = client.query(kind=constants.boats)
        q_limit = int(request.args.get('limit', '2'))
        q_offset = int(request.args.get('offset', '0'))
        l_iterator = query.fetch(limit= q_limit, offset=q_offset)
        pages = l_iterator.pages
        results = list(next(pages))
        if l_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
        output = {"boats": results}
        if next_url:
            output["next"] = next_url
        return json.dumps(output)
    else:
        return 'Method not recogonized'

@bp.route('/<id>', methods=['PUT','DELETE'])
def boats_put_delete(id):
    if request.method == 'PUT':
        content = request.get_json()
        boats_key = client.key(constants.boats, int(id))
        boats = client.get(key=boats_key)
        boats.update({"name": content["name"], "description": content["description"],
          "price": content["price"]})
        client.put(boats)
        return ('',200)
    elif request.method == 'DELETE':
        key = client.key(constants.boats, int(id))
        client.delete(key)
        return ('',200)
    else:
        return 'Method not recogonized'

@bp.route('/<bid>/loads/<lid>', methods=['PUT','DELETE'])
def add_delete_reservation(bid,lid):
    if request.method == 'PUT':
        boats_key = client.key(constants.boats, int(bid))
        boats = client.get(key=boats_key)
        loads_key = client.key(constants.loads, int(lid))
        loads = client.get(key=loads_key)
        if 'loads' in boats.keys():
            boats['loads'].append(loads.id)
        else:
            boats['loads'] = [loads.id]
        client.put(boats)
        return('',200)
    if request.method == 'DELETE':
        boats_key = client.key(constants.boats, int(bid))
        boats = client.get(key=boats_key)
        if 'loads' in boats.keys():
            boats['loads'].remove(int(lid))
            client.put(boats)
        return('',200)

@bp.route('/<id>/loads', methods=['GET'])
def get_reservations(id):
    boats_key = client.key(constants.boats, int(id))
    boats = client.get(key=boats_key)
    loads_list  = []
    if 'loads' in boats.keys():
        for lid in boats['loads']:
            loads_key = client.key(constants.loads, int(lid))
            loads_list.append(loads_key)
        return json.dumps(client.get_multi(loads_list))
    else:
        return json.dumps([])
