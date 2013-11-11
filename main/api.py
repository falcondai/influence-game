from flask import Response, request, make_response
from flask.ext.login import login_required, current_user
from bson.objectid import ObjectId
import json
from bson.json_util import dumps

from database import mongo
from main import app


# modify a graph's edges
def _add_edge(graph_id, source_id, target_id, attr):
    return mongo.db.edges.insert({
        'graph_id': ObjectId(graph_id),
        'source': ObjectId(source_id),
        'target': ObjectId(target_id),
        'attr': attr
        }, j=True)

def _remove_edge(graph_id, source_id, target_id):
    return mongo.db.edges.remove({
        'graph_id': ObjectId(graph_id),
        'source': ObjectId(source_id),
        'target': ObjectId(target_id)
        }, j=True)

def _update_edge(graph_id, source_id, target_id, attr):
    return mongo.db.edges.update({
            'graph_id': ObjectId(graph_id),
            '$or': [{
                'source': ObjectId(source_id),
                'target': ObjectId(target_id)
            }, {
                'target': ObjectId(source_id),
                'source': ObjectId(target_id)
            }]
        }, 
        {
            '$set': {
                'attr': attr,
                'source': ObjectId(source_id),
                'target': ObjectId(target_id)
            }
        }, j=True)

def normalize_json(requst):
    if request.mimetype != 'application/json':
        request.json = json.loads(request.data)
        request.mimetype = 'application/json'

# api endpoints
@app.route('/api/edge/add.json', methods=['POST'])
def add_edge():
    normalize_json(request)
    if not current_user.is_anonymous() and current_user.graph_id == request.json['graph_id']:
        return Response(dumps(_add_edge(request.json['graph_id'], request.json['source_id'], request.json['target_id'], request.json['attr'])), mimetype='application/json')
    return make_response(json.dumps({'error': 'you do not the permission to edit this graph'}), 400)
     
@app.route('/api/edge/remove.json', methods=['POST'])
def remove_edge():
    normalize_json(request)
    if not current_user.is_anonymous() and current_user.graph_id == request.json['graph_id']:
        return Response(dumps(_remove_edge(request.json['graph_id'], request.json['source_id'], request.json['target_id'])), mimetype='application/json')
    return make_response(json.dumps({'error': 'you do not the permission to edit this graph'}), 400)

@app.route('/api/edge/update.json', methods=['POST'])    
def update_edge():
    normalize_json(request)
    if not current_user.is_anonymous() and current_user.graph_id == request.json['graph_id']:
        r = _update_edge(request.json['graph_id'], request.json['source_id'], request.json['target_id'], request.json['attr'])
        if r['updatedExisting']:
            return Response(dumps(r), mimetype='application/json')
        else:
            return Response(dumps(r), status=400, mimetype='application/json')
    return make_response(json.dumps({'error': 'you do not the permission to edit this graph'}), 400)
