from bson.objectid import ObjectId
from flask_restful import Resource,request


from Grade.model import GradeModel


class GradeResource(Resource):
    def post():
        student_id = request.form.get('student_id')
        assignment_id = request.form.get('assignment_id')
        grade = request.form.get('grade')

        if not student_id or not assignment_id or not grade:
            return 'Student ID, Assignment ID and Grade Fields Cannot Be Empty', 400
        
        grade = GradeModel(student_id=student_id, assignment_id=assignment_id, grade=grade)
        result = grade.save()
        if not result:
            return 'Grade Not Found', 404
        return str(result.inserted_id), 200
        