from flask import Blueprint
from Grade.functionality import GradeResource
from logger import log_route_io

grade_bp = Blueprint('grade', __name__, url_prefix='/grade')



"""
/post:
    - Description: Handles grade addition.
    - Request Body: Expects a list of ids named 'student_ids', 'assignment_ids', and  list of scores 'scores'.
    - Response: Returns Success Message if addition is successful, or an error message if addition fails.
"""
@grade_bp.route('/post', methods=['POST'])
@log_route_io
def post():
    return GradeResource.post()


"""
/get-average:
    - Description: Handles average grade retrieval.
    - Request Body: Expects 'student_id', list of 'assignment_ids'.
    - Response: Returns average if retrieval is successful, or an error message if retrieval fails.
"""
@grade_bp.route('/get-average', methods=['POST'])
@log_route_io
def get_average():
    return GradeResource.get_average()


""""
/get:
    - Description: Handles grade retrieval.
    - Request Body: Expects 'student_id', list of 'assignment_ids'.
    - Response: Returns grades if retrieval is successful, or an error message if retrieval fails.
"""
@grade_bp.route('/get', methods=['POST'])
@log_route_io
def get():
    return GradeResource.get()