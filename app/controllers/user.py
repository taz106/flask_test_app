from flask import jsonify, request
from flask_restful import Resource
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bson.json_util import dumps
import json

from app import mongo

from app.schema.userSchema import UserSchema
userSchema = UserSchema()

class CommonMethods:
    def serialize(data):
        obj = {}
        for key,val in data.items():
            if key == '_id':
                obj['_id'] = str(data['_id'])
            else:
                obj[key] = val
        return obj

class UserList(Resource, CommonMethods):
    def get(self):
        res = []
        data = {'_id': ""}
        for user in mongo.db.users.find():
            data, error = userSchema.load(user)
            data['_id'] = str(user['_id'])
            res.append(data)
            print(res) 
        return jsonify({"result": res, "status": 200})

    def post(self):
        data = {}
        user,error = userSchema.load(request.json)
        if error:
            return jsonify({"error":error})
        else:
            res = mongo.db.users.insert(user)
            data = CommonMethods.serialize(user)
            return jsonify({'result': data,'status':200})

class User(Resource, CommonMethods):
    def get(self, userId):
        user = {}
        data = {}
        try:
            user = mongo.db.users.find_one({'_id': ObjectId(userId)})
            print("user: {0} ".format(user))
        except InvalidId as err:
            return {"error": str(err)}
        if user is None:
            return {"error": "No user found having this {0} id ".format(userId)}
        else:
            data = CommonMethods.serialize(user)
        print("data: {0} ".format(data))
        return jsonify({'result': data,'status':200})

    def delete(self, userId):
        try:
            res = mongo.db.users.remove({'_id': ObjectId(userId)})
            print(res)
            if res["n"] == 0:
                return jsonify({"message": "No user to delete having this {0} id ".format(userId)})
            else:
                return jsonify({'result': res,'status':200})
        except InvalidId as err:
            return {"error": str(err)}

    def put(self, userId):
        user = request.json
        query = {"$set" : user}
        try:
            res = mongo.db.users.update({'_id': ObjectId(userId)}, query)
            if res["n"] == 0:
                return jsonify({"message": "No user to delete having this {0} id ".format(userId)})
            else:
                return jsonify({'result': res,'status':200}) 
        except InvalidId as err:
            return {"error": str(err)}