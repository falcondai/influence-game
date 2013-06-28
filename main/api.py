from flask import Response, request
from flask.ext.login import login_required
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
		}, w=1)

def _remove_edge(graph_id, source_id, target_id):
	return mongo.db.edges.remove({
		'graph_id': ObjectId(graph_id),
		'source': ObjectId(source_id),
		'target': ObjectId(target_id)
		}, w=1)

def _update_edge(graph_id, source_id, target_id, attr):
	# TODO error handling
	_remove_edge(graph_id, source_id, target_id)
	_add_edge(graph_id, source_id, target_id, attr)

def normalize_json(requst):
	if request.mimetype != 'application/json':
		request.json = json.loads(request.data)
		request.mimetype = 'application/json'

# api endpoints
@app.route('/api/edge/add.json', methods=['POST'])
@login_required
def add_edge():
	normalize_json(request)
	return Response(dumps(_add_edge(request.json['graph_id'], request.json['source_id'], request.json['target_id'], request.json['attr'])), mimetype='application/json')
	 
@app.route('/api/edge/remove.json', methods=['POST'])
@login_required
def remove_edge():
	normalize_json(request)
	return Response(dumps(_remove_edge(request.json['graph_id'], request.json['source_id'], request.json['target_id'])), mimetype='application/json')

@app.route('/api/edge/update.json', methods=['POST'])	
@login_required
def update_edge():
	normalize_json(request)
	return Response(dumps(_update_edge(request.json['graph_id'], request.json['source_id'], request.json['target_id'], request.json['attr'])), mimetype='application/json')
