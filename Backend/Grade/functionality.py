from bson.objectid import ObjectId
from flask_restful import Resource,request
from datetime import datetime

from Grade.model import GradeModel


class GradeResource(Resource):
    def post():
        student_ids = request.form.getlist('student_ids')
        assignment_ids = request.form.getlist('assignment_ids')
        scores = request.form.getlist('scores')
        
        if not student_ids or not assignment_ids or not scores:
            return 'Student IDs, Assignment IDs And Grades Fields Cannot Be Empty', 400
        if len(student_ids) != len(assignment_ids) or len(student_ids) != len(scores):
            return 'Student ID, Assignment ID And Grade Fields Must Be The Same Length', 400
        
        num_of_grades = len(student_ids)
        for i in range(num_of_grades):
            student_id = student_ids[i]
            assignment_id = assignment_ids[i]
            score = scores[i]

            if not student_id or not assignment_id or not score:
                return 'Student ID, Assignment ID And Grade Fields Cannot Be Empty', 400
            
            if not ObjectId.is_valid(student_id):
                return 'Invalid Student ID', 400
            
            if not ObjectId.is_valid(assignment_id):
                return 'Invalid Assignment ID', 400

            if score!=str(0):
                score = int(score)
                if not (1 <= score <= 100):
                    return 'Grade must be between 1 and 100', 400
            else: score = 0
            date = datetime.now().strftime("%d.%m.%Y")
            grade = GradeModel(student_id=student_id, assignment_id=assignment_id, score=score, date=date)
            result = grade.find()
            if result:
                print('found')
                result = grade.update()
            else: result = grade.save()
            if not result:
                return 'Grade Not Found', 404
            
        return "Grades Added Succesfully", 200
    
    def get():
        student_id = request.args.getlist('student_id')
        assignment_id = request.args.getlist('assignment_id')
        if not student_id or not assignment_id:
            return 'Student IDs And Assignment IDs Cannot Be Empty', 400
        if not ObjectId.is_valid(student_id):
            return 'Invalid Student ID', 400
        if not ObjectId.is_valid(assignment_id):
            return 'Invalid Assignment ID', 400

        grade = GradeModel(student_id=student_id, assignment_id=assignment_id)
        result = grade.find()
        if not result:
            return 'Grade Not Found', 404
        return result['score'], 200