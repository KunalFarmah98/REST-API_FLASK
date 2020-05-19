from flask import Flask
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from Resources.item import Item,ItemList
import datetime

import os

from Resources.user import UserRegister, User, UserLogin
from Models.user import UserModel
from Models.item import ItemModel

from Resources.store import Store,StoreList

app = Flask(__name__)

# setting app secret key
app.secret_key = 'farmahg'

# turning off Flask_SQLAlchemy tracking extension to save computing resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# setting database uri, works with all type of sql distros
# os.environ.get('DATABASE_URL') helps in using postgrace in heroku while also lets us use sqlite as default
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL','sqlite:///data.db')

# Allowing app to show exceptions instead of a simple 500 error
app.config['PROPAGATE_EXCEPTIONS']=True

# Creating an api to add resources to
api = Api(app)

# it is moved to run.py to make sure imports are handled correctly
# @app.before_first_request
# def create_tables():
#     db.create_all()

# Creating a JWTManager for auth
jwt = JWTManager(app)
# it will not create any endpoint



api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')

# setting token expiration time
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=1800)




if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)