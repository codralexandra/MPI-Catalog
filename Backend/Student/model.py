from db_utils import db_database
from bson.objectid import ObjectId

collection = db_database.get_collection('Student')
class StudentModel():
    def __init__(self, first_name=None, last_name=None,_id=None):
        self.first_name = first_name
        self.last_name = last_name
        self._id = _id

    def __dict__(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
    
    def to_student(student):
        return StudentModel(first_name=student['first_name'], last_name=student['last_name'], _id=student['_id'])
    
    def save(self):
        result = collection.insert_one(self.__dict__())
        return result if result else None
    
    def get(self):
        result = collection.find_one({'_id':ObjectId(self._id)})
        return result if result else None
    
    def delete(self):
        result = collection.delete_one({'_id':ObjectId(self._id)})
        return result if result else None
    
    def get_id(self):
        result = collection.find_one({'first_name':self.first_name, 'last_name':self.last_name})
        return result if result else None
    