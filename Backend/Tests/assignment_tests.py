import unittest
import sys
import os

from flask import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

class AssignmentTests(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()
        self.client.testing = True

    def test_add_assignment_success(self):
        response = self.client.post('/assignment/post', data={
            'course_id': '67e29e52900069427cc4c35a',
            'title': 'Test Assignment',
            'date_start': '2025-04-01',
            'date_end': '2025-04-10'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

        assignment_id = response.data.decode('utf-8').strip()

        self.assertTrue(len(assignment_id) > 0)

        self.client.delete('/assignment/delete', data={
            'assignment_id': assignment_id,
        })

        print("\n✅ Test - Successful Assignment Addition")


    def test_get_assignment_success(self):
        get_response = self.client.post('/assignment/get', data={
            'assignment_id': '67eb7f498071b55f16532787'
        })
        
        self.assertEqual(get_response.status_code, 200)
        data = json.loads(get_response.data)
        self.assertEqual(data['title'], 'Multiplications')
        self.assertEqual(data['date_start'], '01.04.2025')
        self.assertEqual(data['date_end'], '04.04.2025')

        print("\n✅ Test - Successful Assignment Get")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    suite.addTest(AssignmentTests('test_add_assignment_success'))
    suite.addTest(AssignmentTests('test_get_assignment_success'))

    runner = unittest.TextTestRunner()
    runner.run(suite)