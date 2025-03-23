from flask_restful import Resource,request
from model import UserModel
from flask import request

class User(Resource):
    def login():
        username = request.form['login']
        password = request.form['pwd']

        return {'role': 'student', 'id': '67dfe103090f6ad84aea4020'}, 200
    
    
    def register():
        username = request.form['username']
        password = request.form['pwd']
        role = request.form['role']
        role = role.lower()

        if not username or not password or not role:
            return 'Username, Password, and Role Fields Cannot Be Empty', 400
        
        if role not in ['student', 'teacher']:
            return 'Role must be either Student or Teacher', 400
        
        user = UserModel(username, password,role)
        user.save()


        return 'Register Completed', 200


