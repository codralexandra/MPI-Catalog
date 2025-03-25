from db_utils import db_database

class Course():
    def __init__(self, course_name, teacher_id, students=None, assigments=None):
        self.collection = db_database.get_collection('Course')
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.students:list['str'] = students #list of student ids
        self.assigments:list['str'] = assigments #list of assigment ids