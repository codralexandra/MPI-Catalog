from flask import Blueprint
from Assignment.functionality import Assignment
from logger import log_route_io
teacher_assignment_bp = Blueprint('assignment', __name__, url_prefix='/assignment/')

"""
/post:
    - Description: Handles assignment addition.
    - Request Body: Expects 'title', 'date_start', and 'date_end'.
    - Response: Returns a the assignment id if addition is successful, or an error message if addition fails.
"""
@teacher_assignment_bp.route('/post', methods=['POST'])
@log_route_io
def post():
    return Assignment.post()

"""
/get:
    - Description: Handles assignment retrieval.
    - Request Body: Expects 'assignment_id'.
    - Response: Returns a list of assignments if retrieval is successful, or an error message if retrieval fails.
"""

@teacher_assignment_bp.route('/get', methods = ['POST'])
@log_route_io
def get():
    return Assignment.get()

"""
/delete:
    - Description: Handles assignment update.
    - Request Body: Expects 'assignment_id'.
    - Response: Returns a success message if delete is successful, or an error message if delete fails.
    - For testing only!
"""
@teacher_assignment_bp.route('/delete', methods=['DELETE'])
@log_route_io
def delete():
    return Assignment.delete()