import os
import sys
import unittest
import json

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database.models import User

class TestUserAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
        with app.app_context():
            db.create_all()
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def test_get_user(self):
        with app.app_context():
            user = User(email="testGET@test.com", password="test", first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        response = self.client.get(f"/get_user/{user.id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"]["email"], user.email)
        self.assertEqual(data["message"]["first_name"], user.first_name)
        self.assertEqual(data["message"]["last_name"], user.last_name)

    def test_verify_user(self):
        with app.app_context():
            user = User(email="testVER@test.com", password="test", first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        data = {"email": user.email, "password": "test"}
        response = self.client.post("/verify_user", json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertTrue(data["result"])

    def test_create_user(self):
        data = {
            "email": "test@test.com",
            "password": "test",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890"
        }
        response = self.client.post("/create_user", json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "New User Added")

    def test_update_user(self):
        with app.app_context():
            user = User(email="testUPD@test.com", password="test", first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        data = {
            "password": "new_password",
            "first_name": "Jane",
            "last_name": "Doe",
            "phone_number": "1234567890"
        }
        response = self.client.put(f"/update_user/{user.id}", json=data)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "User Updated")

    def test_delete_user(self):
        with app.app_context():
            user = User(email="testDEL@test.com", password="test", first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)

        response = self.client.delete(f"/delete_user/{user.id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "User Deleted")

if __name__ == '__main__':
    unittest.main()
