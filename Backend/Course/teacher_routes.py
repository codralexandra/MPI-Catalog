from flask import Blueprint, url_for
from Course.functionality import Course
from flask_restful import request
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
@teacher_course_bp.route('/get', methods=['POST'])
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
/get-assignments:
    - Description: Handles assignment retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns a list of assignments if retrieval is successful, or an error message if retrieval fails.
"""
@teacher_course_bp.route('/get-assignments', methods=['POST'])
def get_assignments():
    assignment_ids ,code = Course.get_assignments()
    if code == 404:
        return 'No Assignments Found', 404
    assignaments_url = url_for('assignment.get', _external=True)
    assignamets_info = []
    for assignment_id in assignment_ids:
        response = requests.post(assignaments_url, data={'assignment_id': assignment_id})
        if response.status_code != 200:
            return 'Something Went Wrong', response.status_code
        assignamets_info.append(response.json())
    return assignamets_info, 200
    

"""
/get-students:
    - Description: Handles student retrieval.
    - Request Body: Expects 'course_id'.
    - Response: Returns a list of students if retrieval is successful, or an error message if retrieval fails.
"""
@teacher_course_bp.route('/get-students', methods=['POST'])
def get_students():
    student_ids,code = Course.get_students()
    if code != 200:
        return 'No Student ID Provided', 400
    student_info_url = url_for('student_info_bp.get_bulk_info', _external=True)
    response = requests.post(student_info_url, data={'student_ids': student_ids})
    if response.status_code != 200:
        return 'Something Went Wrong', response.status_code
    return response.json(), 200


"""
/add-student:
    - Description: Handles student addition.
    - Request Body: Expects 'course_id' and 'first_name', 'last_name'.
    - Response: Returns a success message if addition is successful, or an error message if addition fails.
"""
@teacher_course_bp.route('/add-student', methods=['POST'])
def add_student():
    # get student id from the studen table
    student_info_url = url_for('student_info_bp.get_id', _external=True)
    response = requests.post(student_info_url, data={'first_name': request.form.get('first_name'), 'last_name': request.form.get('last_name') })
    #add it if it is good
    if response.status_code != 200:
        return 'Student Not Found', 404
    student_id = response.text
    message, code =  Course.add_student(student_id)
    if code!= 200:
        return message, code
    return student_id, 200


""""
/remove-student:
    - Description: Handles student removal.
    - Request Body: Expects 'course_id' and 'student_id'.
    - Response: Returns a success message if removal is successful, or an error message if removal fails.
"""
@teacher_course_bp.route('/remove-student', methods=['DELETE'])
def remove_student():
    return Course.remove_student()


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


