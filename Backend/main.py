import sys
import os
# Add the sub-folders to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'User'))

from flask import Flask, request
from flask_cors import CORS
from User.functionality import User


name = 'Gradebook'
app = Flask(name)
CORS(app, origins="http://localhost:3000")


@app.route('/')
def index():
    return 'Welcome to the Gradebook!'


"""
/login:
    - Description: Handles user login.
    - Request Body: Expects 'login' and 'pwd' parameters.
    - Response: Returns the user ID and role if found in the database, or an error message and code if not found.
"""
@app.route('/login', methods=['POST'])
def login():
    return User.login()
    
    
"""
/register:
    - Description: Handles user registration.
    - Request Body: Expects 'username', 'role' and 'pwd' parameters.
    - Response: Returns a success message if registration is successful, or an error message if registration fails.
"""
@app.route('/register', methods=['POST'])
def register():
    return User.register()

"""
/reset_password:
    - Description: Handles password reset.
    - Request Body: Expects 'login', 'new_pwd' and 'old_pwd' parameters.
    - Response: Returns a success message if reset is successful, or an error message if the user is not found.
"""
@app.route('/reset_password', methods=['POST'])
def reset_password():
    return User.reset_password()

if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')

