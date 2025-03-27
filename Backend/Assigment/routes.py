from flask import Blueprint
from Assigment.functionality import Assigment

assigment_bp = Blueprint('assigment', __name__, url_prefix='/assigment/teacher')

"""
/add:
    - Description: Handles assigment addition.
    - Request Body: Expects 'course_id', 'title', 'date_start', and 'date_end'.
    - Response: Returns a the assigment id if addition is successful, or an error message if addition fails.
"""
@assigment_bp.route('/add', methods=['POST'])
def add():
    return Assigment.add()