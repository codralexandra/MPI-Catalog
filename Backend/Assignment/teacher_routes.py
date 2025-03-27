from flask import Blueprint
from Assignment.functionality import Assignment

teacher_assignment_bp = Blueprint('assignment', __name__, url_prefix='/assignment/teacher')

"""
/add:
    - Description: Handles assignment addition.
    - Request Body: Expects 'course_id', 'title', 'date_start', and 'date_end'.
    - Response: Returns a the assignment id if addition is successful, or an error message if addition fails.
"""
@teacher_assignment_bp.route('/add', methods=['POST'])
def add():
    return Assignment.post()

"""
/get:
    - Description: Handles assignment retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns a list of assignments if retrieval is successful, or an error message if retrieval fails.
"""
@teacher_assignment_bp.route('/get', methods = ['GET'])
def get():
    return Assignment.get()


"""
/update:
    - Description: Handles assignment update.
    - Request Body: Expects 'assignment_id', 'title', 'date_start', and 'date_end'.
    - Response: Returns a success message if update is successful, or an error message if update fails.
"""
@teacher_assignment_bp.route('/update', methods=['DELETE'])
def delete():
    return Assignment.delete()