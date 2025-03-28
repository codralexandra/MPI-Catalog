from db_utils import db_database
from bson.objectid import ObjectId

class CourseModel():
    def __init__(self, course_name, teacher_id, students=[], assigments=[], id=None):
        self.collection = db_database.get_collection('Course')
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.students:list['str'] = students #list of student ids
        self.assigments:list['str'] = assigments #list of assigment ids
        self.id = id

    def __dict__(self):
        return {
            'course_name': self.course_name,
            'teacher_id': self.teacher_id,
            'students': self.students,
            'assigments': self.assigments
        }
    
    def to_id_name(self):
        return {
        "id": str(self.id),
        "course_name": self.course_name
        }

    def save(self):
        result = self.collection.insert_one(self.__dict__())
        if result is None:
            return 'Course Not Added', 400
        return result.inserted_id, 200        

    def get_all_with_specific_teacher(self) -> tuple[list['CourseModel'], int]:
        coursesJSON = self.collection.find({'teacher_id': self.teacher_id})
        if not coursesJSON:
            return 'No Courses Found', 404
        courses = []
        for course in coursesJSON:
            course = self.to_course(course)
            courses.append(course)
        return courses, 200

    def get_one(self):
        course = self.collection.find_one({'_id': ObjectId(self.id)})
        if not course:
            return 'Course Not Found', 404
        return self.to_course(course), 200
    

    def to_course(self, course):
        aux = CourseModel(
            course['course_name'],
            course['teacher_id'],
            course['students'],
            course['assigments'],
            course['_id']
        )
        return aux
    
    # uwu only for testing
    def delete(self):
        result = self.collection.delete_one({'_id': ObjectId(self.id)})
        
        if result.deleted_count == 0:
            return 'Course Not Found', 404
        
        return f'Course with ID {self.id} deleted successfully', 200
    
    def get_students(self):
        course = self.collection.find_one({'_id': ObjectId(self.id)})
        if not course:
            return 'Course Not Found', 404
        return course['students'], 200
    

    def get_assignments(self):
        course = self.collection.find_one({'_id': ObjectId(self.id)})
        if not course:
            return 'Course Not Found', 404
        return course['assigments'], 200
    

    def remove_student(self, student_id):
        result = self.collection.update_one(
            {'_id': ObjectId(self.id)},
            {'$pull': {'students': student_id}}
        )
        if result.modified_count == 0:
            return 'Student Not Found', 404
        return 'Student Removed Successfully', 200
    
    def add_student(self, student_id):
        course = self.collection.find_one({'_id': ObjectId(self.id)})
        if not course:
            return 'Course Not Found', 404
        if 'students' not in course or course['students'] is None:
            self.collection.update_one(
                {'_id': ObjectId(self.id)},
                {'$set': {'students': []}}
            )
        result = self.collection.update_one(
            {'_id': ObjectId(self.id)},
            {'$push': {'students': student_id}}
        )
        if result.modified_count == 0:
            return 'Student Not Added', 400
        return 'Student Added Successfully', 200
