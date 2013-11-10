from flask.ext.login import LoginManager, UserMixin
from bson.objectid import ObjectId
from Crypto import Random, Hash

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
        self.salt = user_dict['salt']
        self.password_hash = user_dict['password_hash']
        self.graph_id = unicode(user_dict['graph_id'])
        self.obj = user_dict

    @staticmethod
    def create_user(name, password, salt_byte_length=32):
        try:
            # create an empty graph and obtain its id
            gid = mongo.db.graphs.insert({}, j=True)
            salt = Random.get_random_bytes(salt_byte_length).encode('hex')
            return mongo.db.users.insert({
                'name': name,
                'salt': salt,
                'password_hash': User.hash_password(salt, password), 
                'active': True,
                'graph_id': gid
                }, j=True)
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
        if user and User.hash_password(user.salt, password) == user.password_hash:
            return user
        return None

    @staticmethod
    def hash_password(salt, password):
        return Hash.SHA256.new(salt + password).hexdigest()

@login_manager.user_loader
def load_user(user_id):
    return User.find_user_by_id(user_id)
