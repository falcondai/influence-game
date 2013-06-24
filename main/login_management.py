from flask.ext.login import LoginManager, UserMixin
from bson.objectid import ObjectId

from main import app
from database import mongo

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
	def __init__(self, user_dict):
		self.id = unicode(user_dict[u'_id'])
		self.name = user_dict['name']
		self.graph_id = unicode(user_dict['graph_oid'])
		self.obj = user_dict

@login_manager.user_loader
def load_user(user_id):
	return User(mongo.db.users.find_one({u'_id': ObjectId(user_id)}))
