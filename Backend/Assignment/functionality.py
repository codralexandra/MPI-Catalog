from Assignment.model import AssignmentModel
from flask_restful import request,Resource


class Assignment(Resource):
    def post():
        course_id = request.form.get('course_id')
        title = request.form.get('title')
        date_start = str(request.form.get('date_start'))
        date_end = str(request.form.get('date_end'))

        if not course_id or not title or not date_start or not date_end:
            return 'Course ID, Title, Date Start and Date End Fields Cannot Be Empty', 400
        
        assigment = AssignmentModel(course_id=course_id, title=title, date_start=date_start, date_end=date_end)
        id,code = assigment.save()
        return str(id), code
    
    def get():
        coruse_id = request.form.get('course_id')

        if not coruse_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        _ = AssignmentModel(coruse_id)
        assigments,code = _.get_all_with_specific_course()

        if code == 404:
            return 'Assignments Not Found', 404
        
        assigments = [assigment.__dict__() for assigment in assigments]

        return assigments, 200
    
    def delete():
        assignment_id = request.form.get('assignment_id')

        if not assignment_id:
            return 'Assignment ID', 400
        
        assigment = AssignmentModel(_id=assignment_id)
        code = assigment.delete()
        if code == 404:
            return 'Assignment Not Found', 404
        return 'Assignment Deleted', 200
