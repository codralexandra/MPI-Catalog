from flask_restful import Resource,request

from Student.model import StudentModel


class Student(Resource):
    def post():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        if not first_name or not last_name:
            return 'First Name and Second Name Fields Cannot Be Empty', 400
        
        student = StudentModel(first_name=first_name, last_name=last_name)
        result = student.save()
        if result is None:
            return 'Student Not Added', 400
        return str(result.inserted_id), 200
    
    def get_bulk_info():
        student_ids = request.form.getlist('student_ids')
        students:list['StudentModel'] = []
        if not student_ids:
            return 'No Student ID Provided', 400
        
        for student_id in student_ids:
            if not student_id:
                continue
            student = StudentModel(_id=student_id)
            result = student.get()
            if not result:
                continue
            student = StudentModel.to_student(result)
            student = student.__dict__()
            student['id'] = str(student_id)
            students.append(student)
        return students, 200
    
    def delete():
        student_id = request.form.get('student_id')
        if not student_id:
            return 'Student ID Field Cannot Be Empty', 400
        student = StudentModel(_id=student_id)
        result = student.delete()
        if result is None:
            return 'Student Not Found', 404
        return 'Student Deleted', 200
    
    def get_id():
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        first_name = first_name.lower().strip() if first_name else first_name
        last_name = last_name.lower().strip() if last_name else last_name

        if not first_name or not last_name:
            return 'First Name and Last Name Fields Cannot Be Empty', 400
        
        student = StudentModel(first_name=first_name, last_name=last_name)
        result = student.get_id()
        if not result:
            return 'Student Not Found', 404
        return str(result['_id']), 200
