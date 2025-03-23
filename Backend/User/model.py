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
        self.collection.insert_one(dict)
        return 200
    
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
    
    def find(self):
        user = self.collection.find_one({'username': self.username})
        if user:
            if user['password'] == self.password:
                return user
        return user

