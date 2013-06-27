from flask import Response, request
from flask.ext.login import login_required
from bson.objectid import ObjectId
import json
from bson.json_util import dumps

from database import mongo
from main import app


# modify a graph's links
def _add_link(graph_id, source_id, target_id, attr):
	return mongo.db.graphs.update({'_id': ObjectId(graph_id)}, 
		{'$push': {'links': {'source': ObjectId(source_id), 'target': ObjectId(target_id), 'attr': attr}}}, w=1)
	#mongo.db.get_last_error()

def _remove_link(graph_id, source_id, target_id):
	return mongo.db.graphs.update({'_id': ObjectId(graph_id)}, 
		{'$pull': {'links': {'source': ObjectId(source_id), 'target': ObjectId(target_id)}}}, w=1)

# api endpoints
@app.route('/api/link/add.json', methods=['POST'])
@login_required
def add_link():
	if request.mimetype != 'application/json':
		request.json = json.loads(request.data)
	return Response(dumps(_add_link(request.json['graph_id'], request.json['source_id'], request.json['target_id'], request.json['attr'])), mimetype='application/json')
	 
@app.route('/api/link/remove.json', methods=['POST'])
@login_required
def remove_link():
	if request.mimetype != 'application/json':
		request.json = json.loads(request.data)
	return Response(dumps(_remove_link(request.json['graph_id'], request.json['source_id'], request.json['target_id'])), mimetype='application/json')

@app.route('/api/test')
def api_test():
	return 'api test'