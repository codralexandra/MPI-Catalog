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
    message,code = Course.get_student_courses()
    if code != 200:
        return message, code
    return message, code