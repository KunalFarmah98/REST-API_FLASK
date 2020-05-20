import sqlite3
from flask import Flask
from flask_restful import Resource
from Models.store import StoreModel
from flask_jwt_extended import  jwt_required,get_jwt_claims,fresh_jwt_required



class Store(Resource):

    def get(self,name):
        store = StoreModel.find_by_name(name)
        if(store):
            return store.json(),200
        return {"message": "Store not Found"}

    @fresh_jwt_required
    def post(self,name):
        if (StoreModel.find_by_name(name)):
            return {"message": "Store {} already present".format(name)}
        
        store= StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": 'An error occured while inserting data'},500

        return store.json(),201

    # making delete operation admin only
    @jwt_required
    def delete(self,name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin privileges required for this operation'}
        store = StoreModel.find_by_name(name)
        if(store):
            store.delete_from_db()
        else:
            return {'message': 'Store not found'}
        return {'message': 'Store Delted'}



class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store  in StoreModel.find_all()]} # wrapping query.all() in a function
