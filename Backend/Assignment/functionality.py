from Assignment.model import AssignmentModel
from flask_restful import request,Resource

class Assignment(Resource):
    def post():
        title = request.form.get('title')
        date_start = str(request.form.get('date_start'))
        date_end = str(request.form.get('date_end'))

        if not title or not date_start or not date_end:
            return 'Course ID, Title, Date Start and Date End Fields Cannot Be Empty', 400
        
        assigment = AssignmentModel(title=title, date_start=date_start, date_end=date_end)
        result = assigment.save()
        if not result:
            return 'Assignment Not Added', 400
        return str(result.inserted_id), 200
    
    def get():
        assignment_id = request.form.get('assignment_id')
        if not assignment_id:
            return 'Course ID Field Cannot Be Empty', 400
        assignment = AssignmentModel(_id=assignment_id)
        result = assignment.get()
        if not result:
            return 'Assignment Not Found', 404
        result['id'] = str(result.pop('_id'))
        return result, 200
    
    def delete():
        assignment_id = request.form.get('assignment_id')
        if not assignment_id:
            return 'Assignment ID', 400
        
        assigment = AssignmentModel(_id=assignment_id)
        result = assigment.delete()
        if not result:
            return 'Assignment Not Found', 404
        return 'Assignment Deleted', 200
        