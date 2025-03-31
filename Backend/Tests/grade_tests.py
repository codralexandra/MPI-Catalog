import unittest

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

class GradeTests(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()
        self.client.testing = True
    
    def test_add_grade_success(self):
        student_ids = ['67e53c5960f8a5d53171ec46']
        assignment_ids = ['67e7e56f3e25b983ea4a036f']
        scores = ['10']
        response = self.client.post('/grade/post', data={
            'student_ids': '67e29e52900069427cc4c35a',
            'assignment_ids': assignment_ids,
            'scores': scores
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

        # Finish when a delete route is added
        # self.client.delete('/grade/delete', data={
        #     'grade_id': 'miaumiau',
        # })

        print("\n✅ Test - Successful Assignment Addition")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(GradeTests('test_add_grade_success'))

    runner = unittest.TextTestRunner()
    runner.run(suite)