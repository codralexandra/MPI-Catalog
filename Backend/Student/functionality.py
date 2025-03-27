from flask_restful import Resource,request
from Student.model import StudentModel

class Student(Resource):
    def post():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if not first_name or not last_name:
            return 'First Name and Second Name Fields Cannot Be Empty', 400
        
        student = StudentModel(first_name=first_name, last_name=last_name)
        message, code = student.save()
        if code == 400:
            return message, code
        return str(message), code