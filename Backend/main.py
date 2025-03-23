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
    - Method: POST
    - Description: Handles user login.
    - Request Body: Expects 'login' and 'pwd' parameters.
    - Response: Returns the user ID and role if found in the database, or an error message and code if not found.
"""
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('login')
    password = data.get('pwd')
    return User.login(email, password)
    
    
"""
/register:
    - Method: POST
    - Description: Handles user registration.
    - Request Body: Expects 'username', 'role' and 'pwd' parameters.
    - Response: Returns a success message if registration is successful, or an error message if registration fails.
"""
@app.route('/register', methods=['POST'])
def register():
    return User.register()


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')

