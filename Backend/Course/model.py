from db_utils import db_database
from bson.objectid import ObjectId

collection = db_database.get_collection('Course')
class CourseModel:
    def __init__(self, course_name=None, teacher_id=None, students=[], assignments=[], _id=None):
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.students = students if students is not None else []
        self.assignments = assignments if assignments is not None else []
        self._id = _id

    def __dict__(self):
        return {
            'course_name': self.course_name,
            'teacher_id': self.teacher_id,
            'students': self.students,
            'assignments': self.assignments,
        }
    
    def essential_info(self):
        return {
            "id": str(self._id) if self._id else None,
            "course_name": self.course_name
        }
    
    def to_course(course_data:dict) -> 'CourseModel':
        return CourseModel(
            course_name=course_data.get('course_name'),
            teacher_id=course_data.get('teacher_id'),
            students=course_data.get('students', []),
            assignments=course_data.get('assignments', []),
            _id=course_data.get('_id')
        )
    

    def save(self):
        result = collection.insert_one(self.__dict__())
        return result if result else None
    
    def delete(self):
        result = collection.delete_one({'_id': ObjectId(self._id)})
        return result if result else None
    
    def get_teacher_courses(self):
        courses = collection.find({'teacher_id': self.teacher_id})
        return courses if courses else None
    
    def get_one(self):
        result = collection.find_one({'_id': ObjectId(self._id)})
        return result if result else None
    
    def add_entry(self,entry_name, entry_value):
        course = collection.find_one({'_id': ObjectId(self._id)})
        if not course:
            return 'Course Not Found', 404
        if entry_name not in course or course[entry_name] is None:
            collection.update_one(
                {'_id': ObjectId(self._id)},
                {'$set': {entry_name: []}}
            )
        result = collection.update_one(
            {'_id': ObjectId(self._id)},
            {'$push': {entry_name: entry_value}}
        )
        return result if result else None
    
    def remove_entry(self, entry_name, entry_value):
        result = collection.update_one(
            {'_id': ObjectId(self._id)},
            {'$pull': {entry_name: entry_value}}
        )
        return result if result else None
    
    def get_student_courses(self):
        result = collection.find({"students": str(self.students[0])}) 
        return result if result else None
