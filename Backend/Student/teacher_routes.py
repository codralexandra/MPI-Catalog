from flask import Blueprint
from Student.functionality import Student

student_info_bp = Blueprint('student_info_bp', __name__, url_prefix='/student')


"""
/post:
    - Description: Handles student addition.
    - Request Body: Expects 'first_name', 'second_name'.
    - Response: Returns a the student id if addition is successful, or an error message if addition fails.
"""
@student_info_bp.route('/post', methods=['POST'])
def post():
    return Student.post()

"""
/get-bulk-info:
    - Description: Handles student retrieval.
    - Request Body: Expect a list of student_id's named 'student_ids'.
    - Response: Returns a list of the students' first and last name if successful, or an error message if it fails.
"""
@student_info_bp.route('/get-bulk-info', methods=['GET'])
def get_bulk_info():
    return Student.get_bulk_info()

@student_info_bp.route('/delete', methods=['DELETE'])
def delete():
    return Student.delete()