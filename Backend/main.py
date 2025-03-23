import sys
import os
# Add the sub-folders to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'User'))

from flask import Flask
from User.functionality import User


name = 'Gradebook'
app = Flask(name)


@app.route('/')
def index():
    return 'Welcome to the Gradebook!'

@app.route('/login', methods=['GET'])
def login():
    return User.login()
    
    
@app.route('/register', methods=['POST'])
def register():
    return User.register()


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')

