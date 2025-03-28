from db_utils import db_database
from bson.objectid import ObjectId


class StudentModel():
    def __init__(self, first_name=None, last_name=None,_id=None):
        self.collection = db_database.get_collection('Student')
        self.first_name = first_name
        self.last_name = last_name
        self._id = _id

    def __dict__(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }
    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'id': str(self._id)
        }
    def to_student(student):
        return StudentModel(first_name=student['first_name'], last_name=student['last_name'], _id=student['_id'])
    
    def save(self):
        result = self.collection.insert_one(self.__dict__())
        if  result is None:
            return 'Student Not Added', 400
        return result.inserted_id, 200
    
    def get(self):
        student = self.collection.find_one({'_id':ObjectId(self._id)})
        if student is None:
            return None
        return StudentModel.to_student(student)
    
    def delete(self):
        result = self.collection.delete_one({'_id':ObjectId(self._id)})
        if result.deleted_count == 0:
            return 404
        return 200
    
    def get_id(self):
        student = self.collection.find_one({'first_name':self.first_name, 'last_name':self.last_name})
        if student is None:
            return None
        return str(student['_id'])
    
        