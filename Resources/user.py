import sqlite3
from flask_restful import Resource, reqparse
from Models.user import UserModel

# A resource to register a user
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    
    parser.add_argument('username',
                        type = str,
                        required=True,
                        help = "Can't leave username blank"
                        ) 

    parser.add_argument('password',
                        type = str,
                        required=True,
                        help = "Can't leave password blank"
                        ) 


    def post(self):  
        data = UserRegister.parser.parse_args()
        if(UserModel.find_by_username(data['username'])):
            return {"message": "User {} alreay exists".format(data['username'])},401

        user = UserModel(data['username'],data['password'])
        # alternate way of using unpacking
        # user = UserModel(**data)
        user.save_to_db()

        
        return {"message":"Created user {} successfully".format(data['username'])},201

class User(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if(not user):
            return {'message': 'User not found'},404
        return user.json()

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if(not user):
            return {'message': 'User not found'},404
        user.delete_from_db()
        return {'message': 'User {} deleted'.format(user.username)},200

