from flask_restful import Resource,request
from Course.model import CourseModel

class Course(Resource):
    def post():
        teacher_id = request.form.get('teacher_id')
        course_name = request.form.get('course_name')

        if not teacher_id or not course_name:
            return 'Teacher ID and Course Name Fields Cannot Be Empty', 400
        
        course = CourseModel(teacher_id=teacher_id, course_name=course_name)
        message, code = course.save()
        if code == 400:
            return message, code
        return str(message), code
    
    # uwu only for testing again
    def delete():
        """Delete a course by course_id."""
        course_id = request.form.get('course_id')

        if not course_id:
            return 'Course ID is required to delete a course', 400

        course = CourseModel(course_name=None, teacher_id=None, students=None, assigments=None, id=course_id)

        result, status_code = course.delete()

        return result, status_code        


    def get():
        teacher_id = request.form.get('teacher_id')
        if not teacher_id:
            return 'Teacher ID Field Cannot Be Empty', 400

        coruseModel = CourseModel(None,teacher_id)
        courseModels,code = coruseModel.get_all_with_specific_teacher()
        
        if code != 200:
            return 'Something Went Wrong', code
        
        courses = []
        for course in courseModels:
            course = course.to_id_name()
            courses.append(course)

        return courses, code
    

    def get_one():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        aux = CourseModel(None,None,id=course_id)
        course,code = aux.get_one()
        
        if not course:
            return 'Course Not Found', 404
        

        return course.to_id_name(), code
    

    def get_students():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        aux = CourseModel(None,None,id=course_id)
        students,code = aux.get_students()
        
        if not students:
            return 'No Students Found', 404
        
        return students, code
    
    def get_assignments():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        aux = CourseModel(None,None,id=course_id)
        assignments,code = aux.get_assignments()
        
        if not assignments:
            return 'No Assignments Found', 404
        
        return assignments, code
        
    def remove_student():
        course_id = request.form.get('course_id')
        student_id = request.form.get('student_id')

        if not course_id or not student_id:
            return 'Course ID and Student ID Fields Cannot Be Empty', 400
        
        aux = CourseModel(None,None,id=course_id)
        message,code = aux.remove_student(student_id)

        return message, code
    
    def add_student(student_id):
        course_id = request.form.get('course_id')
        if not student_id or not course_id:
            return 'Student ID and Course ID Fields Cannot Be Empty', 400
        
        aux = CourseModel(None,None,id=course_id)
        message,code = aux.add_student(student_id)

        return message, code