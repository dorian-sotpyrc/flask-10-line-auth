import os
import tempfile
import unittest

from app import create_app


class AuthFlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(delete=False)
        self.tmp.close()
        self.app = create_app(test_db_path=self.tmp.name)
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def tearDown(self):
        try:
            os.unlink(self.tmp.name)
        except FileNotFoundError:
            pass

    def test_protected_redirects_to_login(self):
        res = self.client.get("/me", follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn("/login", res.headers.get("Location", ""))

    def test_signup_then_access_me(self):
        res = self.client.post("/signup", data={"email": "a@b.com", "password": "password123"}, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        res2 = self.client.get("/me", follow_redirects=True)
        self.assertEqual(res2.status_code, 200)
        self.assertIn(b"Signed in", res2.data)


if __name__ == "__main__":
    unittest.main()
