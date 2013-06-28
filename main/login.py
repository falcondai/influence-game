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
		self.graph_id = unicode(user_dict['graph_oid'])
		self.obj = user_dict

	@staticmethod
	def create_user(name, password):
		u = {
		'name': name, 
		'password': password, 
		'active': True,
		}
		try:
			return mongo.db.users.insert(u, w=1)
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
		if user and password == '123':
			return user
		return None

@login_manager.user_loader
def load_user(user_id):
	return User.find_user_by_id(user_id)
