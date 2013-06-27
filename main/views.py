from flask import render_template, redirect, url_for, request, flash, abort, Response
from flask.ext.login import current_user, login_required, login_user, logout_user
from bson.objectid import ObjectId
import json
from bson.json_util import dumps

from login import login_manager, User
from main import app
from database import mongo

# login manager config
login_manager.login_view = 'login'

def handle_redirect(url):
	return redirect(request.args.get('next') or url)

def login_form_validate(form):
	return form.get('username') and form.get('password')

@app.route('/')
def index():
	graphs = mongo.db.graphs.find({}, {'_id': 1})
	return render_template('index.html', graph_ids=map(lambda x: str(x['_id']), graphs))

# user login flow
@app.route('/signup')
def signup():
	pass

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if login_form_validate(request.form):
			user = User.authenticate_user(request.form.get('username'), 
				request.form.get('password'))
			print user.get_id()
			if user and login_user(user, 
				remember=request.form.get('remember')=='on'):
				flash("Logged in successfully.")
				return handle_redirect(url_for("index"))	
		flash("Logged in unsuccessfully.")

	return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Logged out successfully.')
	return handle_redirect(url_for('index'))

# graph views
@app.route('/view/<graph_id>/<center_node_id>')
@app.route('/view/<graph_id>/')
def view(graph_id, center_node_id=''):
	graph = dumps(_get_graph(graph_id))
	if not graph:
		abort(404)
	if center_node_id == '':
		center_node_id = _get_center_node(graph_id)
	# FIXME use a view-only page
	return render_template('mod.html', graph_id=graph_id, center_node_id=center_node_id, graph=graph, all_nodes=dumps([n for n in mongo.db.nodes.find()]))
	
@app.route('/edit/<graph_id>/<center_node_id>')
@app.route('/edit/<graph_id>/')
@login_required
def edit(graph_id, center_node_id=''):
	graph = dumps(_get_graph(graph_id))
	if not graph:
		abort(404)
	if center_node_id == '':
		center_node_id = _get_center_node(graph_id)
	if current_user.graph_id != graph_id:
		flash('You are not the owner of graph %s.' % graph_id)
		return redirect(url_for('view', graph_id=graph_id, center_node_id=center_node_id))
	return render_template('mod2.html', graph_id=graph_id, center_node_id=center_node_id, graph=graph, all_nodes=dumps([n for n in mongo.db.nodes.find()]))

# helper functions
def _get_graph(graph_id):
	return mongo.db.graphs.find_one({'_id': ObjectId(graph_id)})

def _get_node(node_id):
	return mongo.db.nodes.find_one({'_id': ObjectId(node_id)})
	
# TODO not very useful
def _inflate_graph(graph):
	nodes = []
	for n_oid in graph['node_oids']:
		nodes.append(mongo.db.nodes.find_one({'_id': n_oid}))
	graph['node_oids'] = nodes
	
	return graph
	
def _get_user_by_name(name):
	return mongo.db.users.find_one({'name': name})

def _get_center_node(graph_id):
	g = _get_graph(graph_id)
	if g and len(g['links']) > 0:
		oid = g['links'][0]['source']
		return str(oid)
	return None
	
# AJAX calls
# TODO add status message and wrapper to payload
#@app.route('/save/<graph_id>/ , methods=['PUT'])
@app.route('/api/user/<user_name>.json')
def get_user_json(user_name):
	return Response(dumps(_get_user_by_name(user_name)), mimetype='application/json')

@app.route('/api/graph/<graph_id>.json')
def get_graph_json(graph_id):
	# TODO more efficient way to dump json?
	return Response(dumps(_get_graph(graph_id)), mimetype='application/json')

@app.route('/api/node/<node_id>.json')
def get_node_json(node_id):
	return Response(dumps(_get_node(node_id)), mimetype='application/json')
	
@app.route('/api/all_nodes.json')
def get_all_nodes_json():
	return Response(dumps([n for n in mongo.db.nodes.find()]), mimetype='application/json')

