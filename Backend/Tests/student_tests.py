import unittest
import sys
import os

from flask import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

class StudentTests(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()
        self.client.testing = True
    
    def test_add_student_success(self):
        response = self.client.post('/student/post', data={
            'first_name': 'John',
            'last_name': 'Doe'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

        student_id = response.data.decode('utf-8').strip()
        self.assertTrue(len(student_id) > 0)
        
        self.client.delete('/student/delete', data={'student_id': student_id})
        print("\n✅ Test - Successful Student Addition")


    def test_get_bulk_student_info(self):
        response = self.client.post('/student/post', data={
            'first_name': 'Jane',
            'last_name': 'Smith'
        })
        self.assertEqual(response.status_code, 200)
        student_id = response.data.decode('utf-8').strip()
        
        response = self.client.get('/student/get-bulk-info', data={
            'student_ids': [student_id]
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['first_name'], 'Jane')
        self.assertEqual(data[0]['last_name'], 'Smith')
        
        self.client.delete('/student/delete', data={'student_id': student_id})
        print("\n✅ Test - Successful Student Bulk Get")

    
    def test_delete_student(self):
        response = self.client.post('/student/post', data={
            'first_name': 'Mark',
            'last_name': 'Johnson'
        })
        self.assertEqual(response.status_code, 200)
        student_id = response.data.decode('utf-8').strip()
        
        response = self.client.delete('/student/delete', data={'student_id': student_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8').strip(), 'Student Deleted')
        
        response = self.client.get('/student/get-bulk-info', data={
            'student_ids': [student_id]
        })
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(data), 0)
        print("\n✅ Test - Successful Student Delete")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(StudentTests('test_add_student_success'))
    suite.addTest(StudentTests('test_get_bulk_student_info'))
    suite.addTest(StudentTests('test_delete_student'))

    runner = unittest.TextTestRunner()
    runner.run(suite)