from Assigment.model import AssigmentModel
from flask_restful import request,Resource


class Assigment(Resource):
    def add():
        course_id = request.form.get('course_id')
        title = request.form.get('title')
        date_start = str(request.form.get('date_start'))
        date_end = str(request.form.get('date_end'))

        if not course_id or not title or not date_start or not date_end:
            return 'Course ID, Title, Date Start and Date End Fields Cannot Be Empty', 400
        
        assigment = AssigmentModel(course_id=course_id, title=title, date_start=date_start, date_end=date_end)
        id,code = assigment.save()
        return str(id), code
