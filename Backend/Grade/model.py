from bson.objectid import ObjectId

from db_utils import db_database

collection = db_database.get_collection('Grade')
class GradeModel():
    def __init__(self, _id=None, student_id=None, assignment_id=None, score=None,date=None):
        self.student_id:str = student_id
        self.assignment_id:str = assignment_id
        self.score:int = score
        self.date:str = date
        self._id:ObjectId = _id
        
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'assignment_id': self.assignment_id,
            'score': self.score,
            'date': self.date,
        }
    
    def to_grade(self):
        return GradeModel(
            student_id=self.student_id,
            assignment_id=self.assignment_id,
            score=self.score,
            date=self.date,
        )
    

    def save(self):
        result = collection.insert_one(self.to_dict())
        return result if result else None

    def find(self):
        result = collection.find_one({'student_id': self.student_id, 'assignment_id': self.assignment_id})
        return result if result else None
    
    def update(self):
        result = collection.update_one(
            {'student_id': self.student_id, 'assignment_id': self.assignment_id},
            {'$set': {'score': self.score, 'date': self.date}}
        )
        print(result)
        return result if result else None
    