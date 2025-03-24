import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

class AuthTests(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test."""
        self.client = app.test_client()
        self.client.testing = True

    def test_register_success(self):
        """Test successful user registration."""
        response = self.client.post('/register', data={'username': 'newuser', 'pwd': 'securepass', 'role': 'student'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Register Completed')
        print("\n✅ Test - Succesfull Registration")

    def test_register_invalid_role(self):
        """Test registration with an invalid role."""
        response = self.client.post('/register', data={'username': 'user1', 'pwd': 'pass', 'role': 'admin'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Role must be either Student or Teacher')
        print("\n✅ Test - Invalid Role Registration")

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post('/login', data={'login': 'newuser', 'pwd': 'securepass'})
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIn('role', json_data)
        self.assertIn('id', json_data)
        print("\n✅ Test - Succesfull Login")

        # Delete dummy for login
        delete_response = self.client.post('/delete-user', data={'login': 'newuser'})

    def test_login_missing_fields(self):
        """Test login with missing credentials."""
        response = self.client.post('/login', data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.decode(), 'Username and Password Fields Cannot Be Empty')
        print("\n✅ Test - Missing credentials Login")

if __name__ == '__main__':
    suite = unittest.TestSuite()
    
    suite.addTest(AuthTests('test_register_success'))
    suite.addTest(AuthTests('test_register_invalid_role'))
    suite.addTest(AuthTests('test_login_success'))
    suite.addTest(AuthTests('test_login_missing_fields'))

    runner = unittest.TextTestRunner()
    runner.run(suite)