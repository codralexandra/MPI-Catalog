from flask_restful import Resource,request
from Course.model import CourseModel
from bson.objectid import ObjectId

class Course(Resource):
    def post():
        teacher_id = request.form.get('teacher_id')
        course_name = request.form.get('course_name')
        if not teacher_id or not course_name:
            return 'Teacher ID and Course Name Fields Cannot Be Empty', 400
        
        course = CourseModel(teacher_id=teacher_id, course_name=course_name)
        result = course.save()
        if not result:
            return 'Course Not Added', 400
        return str(result.inserted_id), 200
    
    def delete():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID is required to delete a course', 400
        
        course = CourseModel(_id=course_id)
        result = course.delete()
        if not result or result.deleted_count == 0:
            return 'Course Not Found', 404
        return f'Course with ID {course_id} deleted successfully', 200


    def get():
        teacher_id = request.form.get('teacher_id')
        if not teacher_id:
            return 'Teacher ID Field Cannot Be Empty', 400
        
        courseModel = CourseModel(teacher_id=teacher_id)
        result = courseModel.get_teacher_courses()
        if not result:
            return 'No Corses Found', 404
        courses = []
        for course in result:
            course:CourseModel = CourseModel.to_course(course)
            course = course.essential_info()
            courses.append(course)
        return courses, 200
    
    def get_one():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.get_one()
        if not result:
            return 'Course Not Found', 404
        course:CourseModel = CourseModel.to_course(result)
        return course.essential_info(), 200
    
    def get_students():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.get_one()
        if not result:
            return 'Course Not Found', 404
        return result['students'], 200
    
    def get_assignments():
        course_id = request.form.get('course_id')
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.get_one()
        if not result:
            return 'Course Not Found', 404
        return result['assignments'], 200
    
    def add_student(student_id):
        course_id = request.form.get('course_id')
        if not course_id or not student_id:
            return 'Course ID and Student ID Fields Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.add_entry('students',student_id)
        if not result:
            return 'Student Not Added', 400
        return 'Student Added Successfully', 200
    
    def remove_student():
        course_id = request.form.get('course_id')
        student_id = request.form.get('student_id')
        if not course_id or not student_id:
            return 'Course ID and Student ID Fields Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.remove_entry('students',student_id)
        if not result:
            return 'Student Not Removed', 400
        return 'Student Removed Successfully', 200
    
    def add_assignment(assignment_id):
        course_id = request.form.get('course_id')
        if not course_id or not assignment_id:
            return 'Course ID and Assignment ID Fields Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.add_entry('assignments',assignment_id)
        if not result:
            return 'Assignment Not Added', 400
        return 'Assignment Added Successfully', 200
    
    def remove_assignment():
        course_id = request.form.get('course_id')
        assignment_id = request.form.get('assignment_id')
        if not course_id or not assignment_id:
            return 'Course ID and Assignment ID Fields Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.remove_entry('assignments',assignment_id)
        if not result:
            return 'Assignment Not Removed', 400
        return 'Assignment Removed Successfully', 200
    
    def get_student_courses():
        student_id = request.form.get('student_id')
        if not student_id:
            return 'Student ID Field Cannot Be Empty', 400
        
        course = CourseModel(students=[student_id])
        result = course.get_student_courses()
        if not result:
            return 'No Courses Found', 404
        courses = []
        for course in result:
            course:CourseModel = CourseModel.to_course(course)
            course = course.essential_info()
            courses.append(course)
        return courses, 200
    
    def get_assignments(course_id):
        if not course_id:
            return 'Course ID Field Cannot Be Empty', 400
        
        course = CourseModel(_id=course_id)
        result = course.get_one()
        if not result:
            return 'Course Not Found', 404
        return result['assignments'], 200
    
    


