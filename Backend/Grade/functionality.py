from bson.objectid import ObjectId
from flask_restful import Resource,request
from datetime import datetime

from Grade.model import GradeModel


class GradeResource(Resource):
    def post():
        student_id = request.form.get('student_id')
        assignment_id = request.form.get('assignment_id')
        score = request.form.get('score')

        if not student_id or not assignment_id or not score:
            return 'Student ID, Assignment ID And Grade Fields Cannot Be Empty', 400
        
        if score!=str(0):
            score = int(score)
            if not (1 <= score <= 100):
                return 'Grade must be between 1 and 100', 400
        score = None
        date = datetime.now().strftime("%d.%m.%Y")
        grade = GradeModel(student_id=student_id, assignment_id=assignment_id, score=score, date=date)
        result = grade.save()
        if not result:
            return 'Grade Not Found', 404
        return str(result.inserted_id), 200
        