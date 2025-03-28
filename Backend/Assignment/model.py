from db_utils import db_database
from bson.objectid import ObjectId

class AssignmentModel():
    def __init__(self,title=None,date_start=None,date_end=None,_id=None):
        self.collection = db_database.get_collection('Assigment')
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
    
    def to_dict(self):
        return {
            'title': self.title,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'id': str(self._id)
        }
    
    def to_assignment(assignment):
        return AssignmentModel(
            title=assignment['title'],
            date_start=assignment['date_start'],
            date_end=assignment['date_end'],
            _id=assignment['_id']
        )
    
    def save(self):
        result = self.collection.insert_one(self.__dict__())
        if  result is None:
            return 'Assignment Not Added', 400
        return result.inserted_id, 200
    
    def delete(self):
        result = self.collection.delete_one({'_id': ObjectId(self._id)})
        if result.deleted_count == 0:
            return 404
        return 200
    
    def get(self):
        assignment = self.collection.find_one({'_id': ObjectId(self._id)})
        if assignment is None:
            return None
        return AssignmentModel.to_assignment(assignment)
    


    