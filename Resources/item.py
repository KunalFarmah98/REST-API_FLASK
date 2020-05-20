import sqlite3
from flask import Flask,request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity, fresh_jwt_required

from Models.item import ItemModel

# Every Resource is a Class extending Resource

class Item (Resource):

    # defining a parser t parse only the required request data
    # price of an item
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type=float,
    required = True,
    help = "can't leave this blank vitch")

    # store id of item
    parser.add_argument('store_id',
    type=float,
    required = True,
    help = "Each item must have a store id")

    

    # this makes this endpoint authorization specific
    # we need to send the jwt access token in the header of the request
    # JWT manager doesn't take arguments for decorator
    @jwt_required
    def get(self,name):

        item = ItemModel.find_by_name(name)

        if(item):
            return item.json()
        else:
            return {'message': 'Item not found'},404

    # making post requiring fresh token, that is loging in 
    @fresh_jwt_required
    def post(self,name):

        if(ItemModel.find_by_name(name)):
            return {'message': "Item with name {} already exists".format(name)},400

        data = Item.parser.parse_args()

        new_item = ItemModel(name,data['price'],data['store_id'])
        
        try:
            new_item.save_to_db()
        except:
            return {'message': 'Error inserting item'},500        

        return new_item.json(),201

    # making delete only admin specific
    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin privileges required for this operation'}
        item = ItemModel.find_by_name(name)
        if item:
            item.delte_from_db()
            return {'message': 'deleted item {}'.format(item.name)}
        else:
            return {'message': 'Item not found'}

    @fresh_jwt_required
    def put(self, name):
        # parsing required arguments only instead of entire json
        data = Item.parser.parse_args()
        # data = request.get_json()
        item = ItemModel.find_by_name(name)
        
        if(item):
            item.price = data['price']
        else:
            item = ItemModel(name,data['price'],data['store_id'])

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    # adding option auth to get complete info
    # give limited data for logged out users
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items':items},200
        
        return {'items': [item['name'] for item in items],
                'message': 'Login or provide authorization header to get detailed item information'
                },200

