import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fastapi.testclient import TestClient

from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_unregister_removes_participant(self):
        email = "remove-me@example.edu"

        signup_response = self.client.post(
            "/activities/Chess Club/signup",
            params={"email": email},
        )
        self.assertEqual(signup_response.status_code, 200)

        activities = self.client.get("/activities").json()
        self.assertIn(email, activities["Chess Club"]["participants"])

        delete_response = self.client.delete(
            "/activities/Chess Club/signup",
            params={"email": email},
        )

        self.assertEqual(delete_response.status_code, 200)

        activities = self.client.get("/activities").json()
        self.assertNotIn(email, activities["Chess Club"]["participants"])

    def test_unregister_unknown_participant_returns_404(self):
        response = self.client.delete(
            "/activities/Chess Club/signup",
            params={"email": "missing@example.edu"},
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
