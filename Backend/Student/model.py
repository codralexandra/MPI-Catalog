from db_utils import db_database

class StudentModel():
    def __init__(self, first_name=None, last_name=None,_id=None):
        self.collection = db_database.get_collection('Student')
        self.first_name = first_name
        self.last_name = last_name
        self._id = _id

    def __dict__(self):
        return {
            'first_name': self.first_name,
            'second_name': self.last_name,
        }
    
    def save(self):
        result = self.collection.insert_one(self.__dict__())
        if  result is None:
            return 'Student Not Added', 400
        return result.inserted_id, 200
    
        