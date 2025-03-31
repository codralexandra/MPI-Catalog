from bson.objectid import ObjectId

from db_utils import db_database

collection = db_database.get_collection('Grade')
class GradeModel():
    def __init__(self, _id=None, student_id=None, assignment_id=None, grade=None):
        self.student_id:str = student_id
        self.assignment_id:str = assignment_id
        self.grade:int = grade
        self._id:ObjectId = _id
        
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'assignment_id': self.assignment_id,
            'grade': self.grade,
        }
    
    def to_grade(self):
        return GradeModel(
            student_id=self.student_id,
            assignment_id=self.assignment_id,
            grade=self.grade,
        )
    

    def save(self):
        result = collection.insert_one(self.to_dict())
        return result if result else None

    