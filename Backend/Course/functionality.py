from flask_restful import Resource,request
from Course.model import CourseModel
from flask import request

class Course(Resource):
    def add():
        teacher_id = request.form.get('teacher_id')
        course_name = request.form.get('course_name')

        if not teacher_id or not course_name:
            return 'Teacher ID and Course Name Fields Cannot Be Empty', 400
        

        #find teacher 


        course = CourseModel(teacher_id=teacher_id, course_name=course_name)
        return course.save()



    def get_all():
        teacher_id = request.form.get('teacher_id')

        if not teacher_id:
            return 'Teacher ID Field Cannot Be Empty', 400
        
        #find teacher

        coruseModel = CourseModel(None,teacher_id)
        courseModels,code = coruseModel.get_all_with_specific_teacher()
        
        if code is not 200:
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
        