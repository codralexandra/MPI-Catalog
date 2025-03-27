import unittest
import sys
import os
from bson.objectid import ObjectId
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

class TeacherCourseTests(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()
        self.client.testing = True
    
    def test_get_one_success(self):
        """Test successful course retrieval by course_id."""
        response = self.client.get('/course/teacher/get-one', data={'course_id': '67e29e4c900069427cc4c358'})
        # Don't change this please
        # Needs to be a mongoDB generated ID
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()

        self.assertIn('TEST3', list(json_data.values())) 
        print("\n✅ Test - Successful Course Retrieval")

    def test_get_all_success(self):
        """Test successful retrieval of all courses by teacher_id."""
        teacher_id = '67dfe187cae9f2bf02424746'
    
        response = self.client.get('/course/teacher/get', data={'teacher_id': teacher_id})
    
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()

        self.assertIsInstance(json_data, list)
        self.assertGreater(len(json_data), 0)

        # Checks data format to be correct
        for course in json_data:
            self.assertEqual(len(course), 1)
            self.assertIsInstance(list(course.values())[0], str)
    
        print("\n✅ Test - Successful Course Retrieval by Teacher ID")

    def test_add_course(self):
        """Test adding a course and then deleting it."""
        
        course_data = {
            'teacher_id': '67dfe187cae9f2bf02424746',
            'course_name': 'TEST Course'
        }

        response = self.client.post('/course/teacher/post', data=course_data)
        course_id = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ObjectId.is_valid(course_id))
        
        # I'll delete courses manually until the /add route returns a course_id as well!
        
        delete_response = self.client.delete('/course/teacher/delete', data={'course_id': course_id})
        
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(f'Course with ID {course_id} deleted successfully', delete_response.get_data(as_text=True))
        
        print("\n✅ Test - Add and Delete Course Successful")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    suite.addTest(TeacherCourseTests('test_get_one_success'))
    suite.addTest(TeacherCourseTests('test_get_all_success'))
    suite.addTest(TeacherCourseTests('test_add_course'))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
