from flask import Blueprint
from Course.functionality import Course

teacher_course_bp = Blueprint('course', __name__, url_prefix='/course/teacher')

"""
/get-one:
    - Description: Handles course retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns the course id and name if found, or an error message if no course is found.
"""
@teacher_course_bp.route('/get-one', methods=['POST'])
def get_one():
    return Course.get_one()

"""
/get-all:
    - Description: Handles course retrieval.
    - Request Body: Expects 'teacher_id'.
    - Response: Returns a list of course ids and names if found, or an error message if no courses are found.
"""
@teacher_course_bp.route('/get-all', methods=['POST'])
def get_all():
    return Course.get_all()

"""
/add:
    - Description: Handles course addition.
    - Request Body: Expects 'teacher_id' and 'course_name'.
    - Response: Returns a success message if addition is successful, or an error message if addition fails.
"""
@teacher_course_bp.route('/add', methods=['POST'])
def add():
    return Course.add()


