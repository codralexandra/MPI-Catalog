from db_utils import db_database

class UserModel:
    def __init__ (self, username, password, role=None):
        self.collection = db_database['User']
        self.username = username
        self.password = password
        self._id = None
        self.role = role    #'student' or 'teacher'

    def save(self):
        dict = self.__dict__()
        self.collection.insert_one(dict)
        return 200
    
    def __dict__(self):
        return {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }

