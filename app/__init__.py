from flask import Flask
from flask_restful import Api

# PYMONGO IMPORT AND INITIALIZATION
from flask_pymongo import PyMongo
mongo = PyMongo()

# IMPORT APP CONFIG
from config import Config

# IMPORT CONTROLLERS
from app.controllers.user import UserList, User

def create_app():
    app = Flask(__name__)
    api = Api(app, prefix="/api/v1" )
    
    app.config.from_object(Config)
    app.config['MONGO_HOST'] = '127.0.0.1'
    app.config['MONGO_PORT'] = 27017
    app.config['MONGO_DBNAME'] = 'testAppDb001'

    mongo.init_app(app)

    api.add_resource(UserList, "/user", endpoint="user_all")
    api.add_resource(User, "/user/<userId>", endpoint="user_id")

    return app 