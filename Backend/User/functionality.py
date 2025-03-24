from flask_restful import Resource,request
from model import UserModel
from flask import request

class User(Resource):
    def login():
        username = request.form.get('login')
        password = request.form.get('pwd')
        if not username or not password:
            return 'Username and Password Fields Cannot Be Empty', 400
        
        user = UserModel(username, password)
        user_found,code = user.find()

        if code == 404:
            return 'User Not Found', 404
        if code == 403:
            return 'Incorrect Password', 403
        
        return {'role': user_found['role'], 'id': str(user_found['_id'])}, 200


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
    
    
    def reset_password():
        username = request.form.get('login')
        old_password = request.form.get('old_pwd')
        new_password = request.form.get('new_pwd')
        if not username or not old_password or not new_password:
            return 'Username, Old Password, and New Password Fields Cannot Be Empty', 400
        
        user = UserModel(username, old_password)
        _,code = user.find()
        if code == 404:
            return 'User Not Found', 404
        if code == 403:
            return 'Incorrect Password', 403
        
        code = user.reset_password(new_password= new_password)

        if code == 404:
            return 'Incorrect username or password', 403
        return 'Password Reset Completed', 200

