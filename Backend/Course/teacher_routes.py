from flask import Blueprint, url_for
from Course.functionality import Course
import requests


teacher_course_bp = Blueprint('course', __name__, url_prefix='/course/teacher')

"""
/get-one:
    - Description: Handles course retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns the course id and name if found, or an error message if no course is found.
"""
@teacher_course_bp.route('/get-one', methods=['GET'])
def get_one():
    return Course.get_one()

"""
/get:
    - Description: Handles course retrieval.
    - Request Body: Expects 'teacher_id'.
    - Response: Returns a list of course ids and names if found, or an error message if no courses are found.
"""
@teacher_course_bp.route('/get', methods=['GET'])
def get():
    return Course.get()

"""
/post:
    - Description: Handles course addition.
    - Request Body: Expects 'teacher_id' and 'course_name'.
    - Response: Returns a success message if addition is successful, or an error message if addition fails.
"""
@teacher_course_bp.route('/post', methods=['POST'])
def post():
    return Course.post()

"""
/get-assignmets:
    - Description: Handles assignment retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns a list of assignments if retrieval is successful, or an error message if retrieval fails.
"""
@teacher_course_bp.route('/get-assignmets', methods=['GET'])
def get_assignments():
    return url_for('assignment.get')

"""
/get-students:
    - Description: Handles student retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns a list of students if retrieval is successful, or an error message if retrieval fails.
"""
@teacher_course_bp.route('/get-students', methods=['GET'])
def get_students():
    student_ids,code = Course.get_students()
    if not student_ids:
        return 'No Student ID Provided', 400
    student_info_url = url_for('student_info_bp.get_bulk_info', _external=True)
    response = requests.get(student_info_url, data={'student_ids': student_ids})
    if response.status_code != 200:
        return 'Something Went Wrong', response.status_code
    return response.json(), 200


# uwu only for testing again
"""
/delete:
    - Description: Handles course deletion.
    - Request Body: Expects 'course_id'.
    - Response: Returns a success message if deletion is successful, or an error message if deletion fails.
"""
@teacher_course_bp.route('/delete', methods=['DELETE'])
def delete():
    return Course.delete()


