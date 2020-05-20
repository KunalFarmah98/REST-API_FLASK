from flask import Flask,jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager
from Resources.item import Item,ItemList
import datetime

import os

from blacklist import BLACKLIST

from Resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
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

app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens

# Creating an api to add resources to
api = Api(app)

# it is moved to run.py to make sure imports are handled correctly
# @app.before_first_request
# def create_tables():
#     db.create_all()

# Creating a JWTManager for auth
jwt = JWTManager(app)
# it will not create any endpoint

# setting an admin based on our requirements
# identity is whatever we pass in the create_access_token() method during login
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    # making user with id 1 as admin
    if identity==1:
        return {'is_admin':True}

    return {'is_admin':False}

# This method will check if a token is blacklisted, and will be called automatically when blacklist is enabled
# We blacklist the jti, i.e the token, and not the user such that we can implement log out feature as well
# blacklisting identity will not let that user log back in again and take him to token_revoked_handler
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST  # Here we blacklist particular JWTs that have been created in the past.


# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')
# setting token expiration time
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(seconds=1800)




if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)