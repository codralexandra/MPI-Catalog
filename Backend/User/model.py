import pymongo as pm
from db_utils import db_database

class UserModel:
    def __init__ (self, username, password):
        self.collection = db_database['User']
        self.usename = username
        self.password = password

