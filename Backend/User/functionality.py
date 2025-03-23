from flask_restful import Resource,request
from model import UserModel
from flask import request

class User(Resource):
    
    @staticmethod
    def login(username, password):
        print("LOGIN attempt with:", username, password)  # <-- Add this
        if not username or not password:
            return 'Username and Password Fields Cannot Be Empty', 400
        
        user = UserModel(username, password)
        user_found = user.find()

        print("USER FOUND:", user_found)  # <-- And this

        if not user_found:
            return 'User Not Found', 404
        
        return {'role': user_found['role'], 'id': str(user_found['_id'])}, 200

    
    @staticmethod
    def register():
        username = request.form.get('username')
        password = request.form.get('pwd')
        role = request.form.get('role')
        role = role.lower()

        if not username or not password or not role:
            return 'Username, Password, and Role Fields Cannot Be Empty', 400
        
        if role not in ['student', 'teacher']:
            return 'Role must be either Student or Teacher', 400
        
        user = UserModel(username, password,role)
        user.save()


        return 'Register Completed', 200


