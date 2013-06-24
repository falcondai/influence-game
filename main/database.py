from flask.ext.pymongo import PyMongo
from main import app

mongo = PyMongo(app)
