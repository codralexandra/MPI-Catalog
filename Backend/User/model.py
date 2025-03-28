from db_utils import db_database

class UserModel:
    def __init__ (self, username, password, role=None):
        self.collection = db_database.get_collection('User')
        self.username = username
        self.password = password
        self._id = None
        self.role = role    #'student' or 'teacher'

    def save(self):
        dict = self.to_dict()
        user = self.collection.insert_one(dict)
        if not user:
            return 'User could not be saved',404
        return user.inserted_id ,200
    
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
    
    def find(self):
        user = self.collection.find_one({'username': self.username})
        if not user:
            return None, 404
        if user['password'] == self.password:
            return user, 200
        return None, 403

    def reset_password(self, new_password):
        result = self.collection.update_one(
            {'username': self.username, 'password': self.password},
            {'$set': {'password': new_password}}
        )
        if result.matched_count == 0:
            return 404  
        return 200
    
    def delete(self):
        """Delete the user from the database"""
        result = self.collection.delete_one({'username': self.username})
        if result.deleted_count == 1:
            return 200
        return 404
