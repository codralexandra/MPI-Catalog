from db_utils import db_database
from bson.objectid import ObjectId

collection = db_database.get_collection('Assignment')
class AssignmentModel():
    def __init__(self,title=None,date_start=None,date_end=None,_id=None):
        self.title = title
        self.date_start = date_start
        self.date_end = date_end
        self._id = _id

    def __dict__ (self):
        return {
            'title': self.title,
            'date_start': self.date_start,
            'date_end': self.date_end
        }
    
    def to_assignment(assignment):
        return AssignmentModel(
            title=assignment['title'],
            date_start=assignment['date_start'],
            date_end=assignment['date_end'],
            _id=assignment['_id']
        )
    
    def save(self):
        result = collection.insert_one(self.__dict__())
        return result if result else None
    
    def get(self):
        result = collection.find_one({'_id': ObjectId(self._id)})
        return result if result else None
    
    def delete(self):
        result = collection.delete_one({'_id': ObjectId(self._id)})
        return result if result else None