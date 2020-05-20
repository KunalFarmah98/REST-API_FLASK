import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_claims,
    get_jwt_identity,
    jwt_refresh_token_required,
    get_raw_jwt
)
from blacklist import BLACKLIST
from Models.user import UserModel


_user_parser = reqparse.RequestParser()
    
_user_parser.add_argument('username',
                        type = str,
                        required=True,
                        help = "Can't leave username blank"
                        ) 

_user_parser.add_argument('password',
                        type = str,
                        required=True,
                        help = "Can't leave password blank"
                        ) 
# A resource to register a user
class UserRegister(Resource):

    def post(self):  
        data = _user_parser.parse_args()
        if(UserModel.find_by_username(data['username'])):
            return {"message": "User {} alreay exists".format(data['username'])},401

        user = UserModel(data['username'],data['password'])
        # alternate way of using unpacking
        # user = UserModel(**data)
        user.save_to_db()

        
        return {"message":"Created user {} successfully".format(data['username'])},201

class User(Resource):
    @jwt_required
    def get(self,user_id):
        user = UserModel.find_by_id(user_id)
        if(not user):
            return {'message': 'User not found'},404
        return user.json()
    
    # making deleting a user admin only
    @jwt_required
    def delete(self,user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin Privileges required for this operation'}
        user = UserModel.find_by_id(user_id)
        if(not user):
            return {'message': 'User not found'},404
        elif user.id==1:
            return {'message': 'Can not delete admin'},500
        user.delete_from_db()
        return {'message': 'User {} deleted'.format(user.username)},200

class UserLogin(Resource):
    
    def post(self):
        # gets data from parser
        data = _user_parser.parse_args()
        #  finds user in db
        user = UserModel.find_by_username(data['username'])
        #check password
        if user and user.password == data['password']:
            # creates an access token and a refresh token
            access_token= create_access_token(identity=user.id,fresh=True)
            refresh_token  = create_refresh_token(user.id)

            return{
                'access_token': access_token,
                'refresh_token': refresh_token
            },200

        return{'message':'Invalid User Credentials'},401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        curr_user = get_jwt_identity()
        new_token = create_access_token(identity=curr_user, fresh=False)
        return {'access_token':new_token},200

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        # we blacklist the access token, such that it can't be used again and user has to login again
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200