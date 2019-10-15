from unittest import TestCase

from tests.AppTestBase import AppTestBase

from flask_security import login_user
from src import app


class TestApplication(AppTestBase, TestCase):
    def test_app_info(self):
        with app.test_client() as c:
            rvl = AppTestBase.login(c, self.user.username, self.test_password)
            rv = c.get("/", follow_redirects=False)
            # print(rvl.data)
            # print(rvl.headers)
            # self.assertEqual(rv.status_code, 200)
