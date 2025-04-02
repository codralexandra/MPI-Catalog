from flask import Blueprint
from User.functionality import User

user_bp = Blueprint('user', __name__)


"""
/login:
    - Description: Handles user login.
    - Request Body: Expects 'login' and 'pwd' parameters.
    - Response: Returns the user ID and role if found in the database, or an error message and code if not found.
"""
@user_bp.route('/login', methods=['POST'])
def login():
    return User.login()


"""
/register:
    - Description: Handles user registration.
    - Request Body: Expects 'username', 'role' and 'pwd' parameters.
    - Response: Returns a success message if registration is successful, or an error message if registration fails.
"""
@user_bp.route('/register', methods=['POST'])
def register():
    return User.register()


"""
/reset-password:
    - Description: Handles password reset.
    - Request Body: Expects 'login', 'new_pwd' and 'old_pwd' parameters.
    - Response: Returns a success message if reset is successful, or an error message if the user is not found.
"""
@user_bp.route('/reset-password', methods=['POST'])
def reset_password():
    return User.reset_password()


"""
/delete-user:
    - Description: Handles user deletion (for register testing).
    - Request Body: Expects 'login' parameter.
    - Response: Returns a success message if delete is successful, or an error message if the user is not found.
"""
@user_bp.route('/delete-user', methods=['POST'])
def delete_user():
    return User.delete_user()

