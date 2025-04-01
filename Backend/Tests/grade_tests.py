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
        student_ids = ['67e53c3f60f8a5d53171ec45']
        assignment_ids = ['67ebfbc7a97c28fd3846c0c6']
        scores = ['10']
        response = self.client.post('/grade/post', data={
            'student_ids': student_ids,
            'assignment_ids': assignment_ids,
            'scores': scores
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)

        print("\n✅ Test - Successful Grade Upload")

    def test_add_bulk_success(self):
        student_ids = ['67e53c3f60f8a5d53171ec45', '67e53bd260f8a5d53171ec44']
        assignment_ids = ['67ebfbc7a97c28fd3846c0c6', '67ebfbc7a97c28fd3846c0c6']
        scores = ['3', '3']
        response = self.client.post('/grade/post', data={
            'student_ids': student_ids,
            'assignment_ids': assignment_ids,
            'scores': scores
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data)
        
        print("\n✅ Test - Successful Bulk Grade Upload")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    
    suite.addTest(GradeTests('test_add_grade_success'))
    suite.addTest(GradeTests('test_add_bulk_success'))

    runner = unittest.TextTestRunner()
    runner.run(suite)