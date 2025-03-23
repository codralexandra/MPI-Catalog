import pymongo as pm
from dotenv import load_dotenv
import os


load_dotenv()
db_URL = os.getenv('DB_URL')
db_client = pm.MongoClient(db_URL)
db_database = db_client['Gradebook']