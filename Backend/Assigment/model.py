from db_utils import db_database
from bson.objectid import ObjectId

class AssigmentModel():
    def __init__(self,course_id,title,date_start,date_end,_id=None):
        self.collection = db_database.get_collection('Assigment')
        self.course_id = course_id
        self.title = title
        self.date_start = date_start
        self.date_end = date_end
        self._id = _id

    def __dict__ (self):
        return {
            'course_id': self.course_id,
            'title': self.title,
            'date_start': self.date_start,
            'date_end': self.date_end
        }
    
    def save(self):
        result = self.collection.insert_one(self.__dict__())
        if  result is None:
            return 'Assigment Not Added', 400
        return result.inserted_id, 200

    