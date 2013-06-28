from flask.ext.login import LoginManager, UserMixin
from bson.objectid import ObjectId

from main import app
from database import mongo

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
	def __init__(self, user_dict=None, **kwargs):
		if not user_dict:
			user_dict = kwargs
		self.id = unicode(user_dict[u'_id'])
		self.name = user_dict['name']
		self.password = user_dict['password']
		self.graph_id = unicode(user_dict['graph_id'])
		self.obj = user_dict

	@staticmethod
	def create_user(name, password):
		try:
			gid = mongo.db.graphs.insert({}, w=1)
			return mongo.db.users.insert({
				'name': name, 
				'password': password, 
				'active': True,
				'graph_id': gid
				}, w=1)
		except:	
			return None

	@staticmethod
	def find_user_by_id(user_id):
		user_record = mongo.db.users.find_one({u'_id': ObjectId(user_id)})
		if user_record:
			return User(user_record)
		return None

	@staticmethod
	def find_user_by_name(username):
		user_record = mongo.db.users.find_one({u'name': username})
		if user_record:
			return User(user_record)
		return None

	@staticmethod
	def authenticate_user(username, password):
		user = User.find_user_by_name(username)
		if user and password == user.password:
			return user
		return None

@login_manager.user_loader
def load_user(user_id):
	return User.find_user_by_id(user_id)
