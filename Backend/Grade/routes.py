from flask import Blueprint
from Grade.functionality import GradeResource


grade_bp = Blueprint('grade', __name__, url_prefix='/grade')



"""
/post:
    - Description: Handles grade addition.
    - Request Body: Expects 'student_id', 'assignment_id', and 'grade'.
    - Response: Returns the grade id if addition is successful, or an error message if addition fails.
"""
@grade_bp.route('/post', methods=['POST'])
def post():
    return GradeResource.post()