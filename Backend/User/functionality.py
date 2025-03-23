from flask_restful import Resource,request
from model import UserModel
from flask import request

class User(Resource):
    def login():
        data = request.get_json()
        username = data['login']
        password = data['pwd']
        return 200
    
    def register():
        username = request.form['login']
        password = request.form['pwd']
        role = request.form['role']

        if not username or not password or not role:
            return 'Username, Password, and Role Fields Cannot Be Empty', 400
        
        if role not in ['student', 'teacher']:
            return 'Role must be either Student or Teacher', 400
        
        user = UserModel(username, password,role)
        user.save()


        return 'Register Completed', 200


