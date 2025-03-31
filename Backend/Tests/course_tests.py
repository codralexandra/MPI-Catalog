import unittest
from unittest.mock import patch

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

    # MOCK RESPONSES - ASSIGNMENT
    def mock_assignment_response(*args, **kwargs):
        """Mock response for assignment retrieval."""
        class MockResponse:
            status_code = 200
            def json(self):
                return {"assignment_id": kwargs['data']['assignment_id'], "details": "Mocked Assignment"}
        return MockResponse()
    
    def mock_create_assignment(*args, **kwargs):
        """Mock the assignment creation response."""
        class MockResponse:
            status_code = 200
            text = "mocked_assignment_id"
    
        return MockResponse()
    
    def mock_delete_assignment(*args, **kwargs):
        """Mock response for assignment deletion."""
        class MockResponse:
            status_code = 200
            text = "mocked_assignment_delete"
    
        return MockResponse()
    
    # MOCK RESPONSES - STUDENT
    def mock_student_info_response(*args, **kwargs):
        """Mock the response for getting student information."""
        student_info = [
            {'student_id': 'student1', 'name': 'John Doe', 'email': 'john.doe@example.com'},
            {'student_id': 'student2', 'name': 'Jane Smith', 'email': 'jane.smith@example.com'},
            {'student_id': 'student3', 'name': 'Tom Brown', 'email': 'tom.brown@example.com'}
        ]
    
        class MockResponse:
            status_code = 200
            def json(self):
                return student_info
        
        return MockResponse()

    def mock_get_student_id(*args, **kwargs):
        """Mock the response for getting a student's ID."""
        class MockResponse:
            status_code = 200
            text = str(ObjectId())
    
        return MockResponse()
    
    def mock_add_student(*args, **kwargs):
        """Mock the response for adding a student to the course."""
            
        return "Student added to course", 200
    
    def mock_remove_student(*args, **kwargs):
        """Mock the response for removing a student from the course."""
        
        return "Student Removed Successfully", 200

    # COURSE TESTS
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
    
        response = self.client.post('/course/teacher/get', data={'teacher_id': teacher_id})
    
        # print(response)
        
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()

        self.assertIsInstance(json_data, list)
        self.assertGreater(len(json_data), 0)

        for course in json_data:
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
                
        delete_response = self.client.delete('/course/teacher/delete', data={'course_id': course_id})
        
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn(f'Course with ID {course_id} deleted successfully', delete_response.get_data(as_text=True))
        
        print("\n✅ Test - Add and Delete Course Successful")
    
    # ASSIGNMENT TESTS
    @patch("requests.post", side_effect=mock_assignment_response)
    def test_get_assignments(self, mock_post):
        """Test retrieving assignments for a course."""
        course_id = '67e29e4c900069427cc4c358'
        response = self.client.post('/course/teacher/get-assignments', data={'course_id': course_id})
        self.assertEqual(response.status_code, 200)

        json_data = response.get_json()
        self.assertIsInstance(json_data, list)
        self.assertGreater(len(json_data), 0)

        for assignment in json_data:
            self.assertIn("assignment_id", assignment)
            self.assertIn("details", assignment)

        print("\n✅ Test - Assignments Retrieved Successfully")

    @patch("requests.post", side_effect=mock_create_assignment)
    @patch("requests.delete", side_effect=mock_delete_assignment)
    def test_add_assignment(self, mock_delete, mock_post):
        """Test adding and deleting an assignment for a course."""
        course_id = '67e29e4c900069427cc4c358'
        title = 'TEST ASSIGNMENT'
        date_start = '02.08.2003'
        date_end = '02.08.2003'

        response = self.client.post('/course/teacher/add-assignment', data={
            'course_id': course_id,
            'title': title,
            'date_start': date_start,
            'date_end': date_end
        })

        self.assertEqual(response.status_code, 200)

        assignment_id = response.get_data(as_text=True).strip()
        self.assertEqual(assignment_id, "mocked_assignment_id")

        delete_response = self.client.post('/course/teacher/remove-assignment', data={
            'course_id': course_id,
            'assignment_id': assignment_id
        })

        self.assertEqual(delete_response.status_code, 200)
        self.assertIn("Assignment Removed Successfully", delete_response.get_data(as_text=True))

        print("\n✅ Test - Add and Delete Assignment Successful")

    # STUDENT TESTS
    @patch("requests.post", side_effect=mock_student_info_response)
    def test_get_students(self, mock_post):
        """Test retrieving students for a course."""
        course_id = '67e29e4c900069427cc4c358'
    
        response = self.client.post('/course/teacher/get-students', data={'course_id': course_id})
    
        self.assertIn(response.status_code, [200, 400])

        if response.status_code == 200:
            json_data = response.get_json()
            self.assertIsInstance(json_data, list)
            self.assertEqual(len(json_data), 3)
            self.assertIn('student_id', json_data[0])
            self.assertIn('name', json_data[0])
            self.assertIn('email', json_data[0])
            print("\n✅ Test - Students Retrieved Successfully")
        else:
            self.assertEqual(response.data.decode('utf-8'), 'No Student ID Provided')
            print("\n✅ Test - No Students Found")

    @patch("requests.post", side_effect=mock_get_student_id)
    @patch("Course.model.CourseModel.add_student", side_effect=mock_add_student)
    @patch("Course.model.CourseModel.remove_student", side_effect=mock_remove_student)
    def test_add_student(self, mock_remove_student, mock_add_student, mock_post):
        """Test adding and removing a student to/from a course."""
        course_id = '67e29e4c900069427cc4c358'
        student_data = {
            'first_name': 'test',
            'last_name': 'student',
            'course_id': course_id
        }
        
        response = self.client.post('/course/teacher/add-student', data=student_data)
        
        self.assertIn(response.status_code, [200, 404])

        if response.status_code == 200:
            student_id = response.get_data(as_text=True).strip()
            self.assertTrue(ObjectId.is_valid(student_id))
            print("\n✅ Test - Student Successfully Added to Course")

            remove_response = self.client.post('/course/teacher/remove-student', data={'course_id': course_id, 'student_id': student_id})
            
            self.assertEqual(remove_response.status_code, 200)
            self.assertEqual(remove_response.data.decode('utf-8'), 'Student Removed Successfully')
            print("\n✅ Test - Student Successfully Removed from Course")
        else:
            self.assertEqual(response.data.decode('utf-8'), 'Student Not Found')
            print("\n❎ Test - Student Not Found")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    suite.addTest(TeacherCourseTests('test_get_one_success'))
    suite.addTest(TeacherCourseTests('test_get_all_success'))
    suite.addTest(TeacherCourseTests('test_add_course'))

    # With mocked responeses
    # Following routes call external routes
    suite.addTest(TeacherCourseTests('test_get_assignments'))
    suite.addTest(TeacherCourseTests('test_add_assignment'))
    
    suite.addTest(TeacherCourseTests('test_get_students'))
    suite.addTest(TeacherCourseTests('test_add_student'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
