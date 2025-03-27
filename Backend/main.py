import sys
import os
# Add the sub-folders to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'User'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Assigment'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Teacher'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Student'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Coruse'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Grade'))

from flask import Flask
from flask_cors import CORS
from User.routes import user_bp
from Course.teacher_routes import teacher_course_bp
from Assigment.routes import assigment_bp


name = 'Gradebook'
app = Flask(name)
CORS(app, origins="http://localhost:3000")


app.register_blueprint(user_bp)
app.register_blueprint(teacher_course_bp)
app.register_blueprint(assigment_bp)

@app.route('/')
def index():
    return 'Welcome to the Gradebook!'

if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')


