from flask_restful import Resource
from model import UserModel
from flask import request

class User(Resource):
    def login():
        data = request.get_json()
        username = data['username']
        password = data['password']

        return 200


