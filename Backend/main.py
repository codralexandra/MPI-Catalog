from flask import Flask
from User.functionality import User


name = 'Gradebook'
app = Flask(name)


@app.route('/')
def index():
    return 'Welcome to the Gradebook!'

@app.route('/login')
def login():
    return User.login()
    
    


if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')

