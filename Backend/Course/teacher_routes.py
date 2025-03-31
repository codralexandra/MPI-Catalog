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
/add-assignment:
    - Description: Handles assignment addition.
    - Request Body: Expects 'course_id' and 'title', 'date_start' and 'date_end'.
    - Response: Returns id if addition is successful, or an error message if addition fails."""
@teacher_course_bp.route('/add-assignment', methods=['POST'])
def add_assignment():
    #Creat Assignment
    assignmnets_url = url_for('assignment.post', _external=True)
    result = requests.post(assignmnets_url, data={'title': request.form.get('title'), 'date_start': request.form.get('date_start'), 'date_end': request.form.get('date_end')})
    if result.status_code != 200:
        return 'Assignment could not be created', 404
    assignemnt_id = result.text

    #Add it to the course
    message, code = Course.add_assignment(assignemnt_id)
    if code != 200:
        return message, code
    
    #Create Grade for the assignment
    grade_url = url_for('grade.post', _external=True)
    message,code = Course.get_students()
    if code != 200:
        return message, code
    student_ids = message
    assignemnt_ids = [request.form.get('assignment_id')] * len(student_ids)
    scores = [0] * len(student_ids)
    result = requests.post(grade_url, data={'student_ids': student_ids, 'assignment_ids': assignemnt_ids, 'scores': scores})
    if result.status_code != 200:
        return f'Grade could not be added. Error code {result.text}', 404
    
    return 'Assignment Removed Successfully', 200

"""
/remove-assignment:
    - Description: Handles assignment removal.
    - Request Body: Expects 'course_id' and 'assignment_id'.
    - Response: Returns a success message if removal is successful, or an error message if removal fails.
"""
@teacher_course_bp.route('/remove-assignment', methods=['POST'])
def remove_assignment():
    #Delete the Assignment
    assignments_url = url_for('assignment.delete', _external=True)
    response = requests.delete(assignments_url, data={'assignment_id': request.form.get('assignment_id')})
    if response.status_code != 200:
        return 'Assignment Not Found', 404
    
    #Remove it from the course
    message, code = Course.remove_assignment()
    if code != 200:
        return message, code
    
    #Remove the grades for the assignment
    grade_url = url_for('grade.post', _external=True)
    message, code = Course.get_students()
    if code != 200:
        return message, code
    student_ids = message
    assignemnt_ids = [request.form.get('assignment_id')] * len(student_ids)
    scores = [0] * len(student_ids)
    result = requests.post(grade_url, data={'student_ids': student_ids, 'assignment_ids': assignemnt_ids, 'scores': scores})
    if result.status_code != 200:
        return f'Grade could not be deleted. Error code {result.text}', 404
    
    return 'Assignment Removed Successfully', 200


    

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
    
    #Add Grades for each assignment
    grade_url = url_for('grade.post', _external=True)
    message, code = Course.get_assignments()
    if code != 200:
        return message, code
    assignment_ids = message
    student_ids = [student_id] * len(assignment_ids)
    scores = [0] * len(assignment_ids)
    result = requests.post(grade_url, data={'student_ids': student_ids, 'assignment_ids': assignment_ids, 'scores': scores})
    if result.status_code != 200:
        return f'Grade could not be created. Error code: {result.text}', 404
    
    return 'Student Added Successfully', 200


""""
/remove-student:
    - Description: Handles student removal.
    - Request Body: Expects 'course_id' and 'student_id'.
    - Response: Returns a success message if removal is successful, or an error message if removal fails.
"""
@teacher_course_bp.route('/remove-student', methods=['POST'])
def remove_student():
    message,code= Course.remove_student()
    if code != 200:
        return message, code
    
    #Remove the grades for the assignment
    grade_url = url_for('grade.post', _external=True)
    message, code = Course.get_assignments()
    if code != 200:
        return message, code
    assignemnt_ids = message
    student_ids = [request.form.get('student_ids')] * len(assignemnt_ids)
    scores = [0] * len(assignemnt_ids)
    result = requests.post(grade_url, data={'student_ids': student_ids, 'assignment_ids': assignemnt_ids, 'scores': scores})
    if result.status_code != 200:
        return f'Grade could not be deleted. Error code {result.text}', 404
    
    return 'Student Removed Successfully', 200



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


