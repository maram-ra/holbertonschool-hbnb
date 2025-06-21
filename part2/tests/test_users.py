import unittest
from app.services.facade import HBnBFacade
from app.utils.helpers import generate_uuid

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()

    def test_create_user_success(self):
        data = {
            "id": generate_uuid(),
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        user = self.facade.create_user(data)
        self.assertEqual(user["first_name"], "John")
        self.assertEqual(user["email"], "john.doe@example.com")

    def test_create_user_missing_fields(self):
        data = {
            "id": generate_uuid(),
            "first_name": "",
            "last_name": "",
            "email": "john.doe@example.com"
        }
        with self.assertRaises(ValueError) as ctx:
            self.facade.create_user(data)
        self.assertIn("First name and last name are required", str(ctx.exception))

    def test_create_user_invalid_email(self):
        data = {
            "id": generate_uuid(),
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "not-an-email"
        }
        with self.assertRaises(ValueError) as ctx:
            self.facade.create_user(data)
        self.assertIn("Invalid email format", str(ctx.exception))

    def test_get_user_by_id(self):
        user_data = {
            "id": "user123",
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com"
        }
        self.facade.create_user(user_data)
        user = self.facade.get_user("user123")
        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "test.user@example.com")

    def test_get_user_by_email(self):
        user_data = {
            "id": "user321",
            "first_name": "Test",
            "last_name": "Email",
            "email": "email.user@example.com"
        }
        self.facade.create_user(user_data)
        user = self.facade.get_user_by_email("email.user@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], "user321")

    def test_update_user_success(self):
        user_data = {
            "id": "update123",
            "first_name": "Old",
            "last_name": "Name",
            "email": "update@example.com"
        }
        self.facade.create_user(user_data)
        updated = self.facade.update_user("update123", {"first_name": "New"})
        self.assertEqual(updated["first_name"], "New")

    def test_update_user_nonexistent(self):
        result = self.facade.update_user("missing_id", {"first_name": "DoesNotExist"})
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
