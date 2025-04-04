import sys
import os
# Add the sub-folders to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'User'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Assigment'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Teacher'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Student'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Coruse'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Grade'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'Backup'))

from flask import Flask
from flask_cors import CORS
import logging

from User.routes import user_bp
from Backup.routes import backup_bp
from Course.teacher_routes import teacher_course_bp
from Course.student_routes import student_course_bp
from Assignment.routes import teacher_assignment_bp
from Student.teacher_routes import student_info_bp
from Grade.routes import grade_bp


name = 'Gradebook'
app = Flask(name)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"])
logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Set log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    filemode="w",  # Append mode (use 'w' to overwrite on each run)
)


app.register_blueprint(user_bp)
app.register_blueprint(teacher_assignment_bp)
app.register_blueprint(teacher_course_bp)
app.register_blueprint(student_info_bp)
app.register_blueprint(grade_bp)
app.register_blueprint(student_course_bp)
app.register_blueprint(backup_bp)



@app.route('/')
def index():
    return 'Welcome to the Gradebook!'



if __name__ == '__main__':
    app.run(debug=True, port='5000', host='0.0.0.0')


