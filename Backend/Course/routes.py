from flask import Blueprint
from Course.functionality import Course

course_bp = Blueprint('course', __name__, url_prefix='/course')

"""
/get-one:
    - Description: Handles course retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns a course if found, or an error message if no course is found.
"""
@course_bp.route('/get-one', methods=['POST'])
def get_one():
    return Course.get_one()

"""
/get-all:
    - Description: Handles course retrieval.
    - Request Body: Expects 'teacher_id'.
    - Response: Returns a list of courses if found, or an error message if no courses are found.
"""
@course_bp.route('/get-all', methods=['POST'])
def get_all():
    return Course.get_all()

"""
/add:
    - Description: Handles course addition.
    - Request Body: Expects 'teacher_id' and 'course_name'.
    - Response: Returns a success message if addition is successful, or an error message if addition fails.
"""
@course_bp.route('/add', methods=['POST'])
def add():
    return Course.add()


