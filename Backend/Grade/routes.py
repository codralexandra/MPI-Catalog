from flask import Blueprint
from Grade.functionality import GradeResource


grade_bp = Blueprint('grade', __name__, url_prefix='/grade')



"""
/post:
    - Description: Handles grade addition.
    - Request Body: Expects a list of ids named 'student_ids', 'assignment_ids', and  list of scores 'scores'.
    - Response: Returns Success Message if addition is successful, or an error message if addition fails.
"""
@grade_bp.route('/post', methods=['POST'])
def post():
    return GradeResource.post()


"""
/get:
    - Description: Handles grade retrieval.
    - Request Body: Expects a list of ids named 'student_ids', 'assignment_ids'.
    - Response: Returns Success Message if retrieval is successful, or an error message if retrieval fails.
"""
@grade_bp.route('/get', methods=['GET'])
def get():
    return GradeResource.get()