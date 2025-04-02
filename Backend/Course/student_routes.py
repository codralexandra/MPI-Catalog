from flask import Blueprint, url_for
from Course.functionality import Course
from flask_restful import request
import requests


student_course_bp = Blueprint('student_course', __name__, url_prefix='/course/student')

""""
/get:
    - Description: Handles course retrieval for a student.
    - Request Body: Expects 'student_id' parameter.
    - Response: Returns list of coruses ids, names and avg score, or an error message if not found.
"""
@student_course_bp.route('/get', methods=['POST'])
def get_student_courses():
    returned_value = []
    
    message,code = Course.get_student_courses()
    if code != 200:
        return message, code
    for course in message:
        assignmnet_ids,code = Course.get_assignments(course['id'])
        if code != 200:
            return f'Assignment IDs Not Found {assignmnet_ids}', 404
        
        grade_url = url_for('grade.get_average', _external=True)
        payload = {
            'student_id': request.form.get('student_id'),
            'assignment_ids': assignmnet_ids
        }
        response = requests.post(grade_url, data=payload)
        if response.status_code != 200:
            return f'Error fetching grades, {response.text}', response.status_code
        avg_score = response.json()
        returned_value.append({
            'course_id': course['id'],
            'course_name': course['course_name'],
            'avg_score': avg_score
        })
        
    return returned_value, 200