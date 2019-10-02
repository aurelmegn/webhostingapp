from unittest import TestCase
from src import app


class TestIndex(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_index(self):
        # test login page on non connected user where I expect a redirection
        with app.test_client() as c:
            rv = c.get('/', follow_redirects=False)
            self.assertEqual(rv.status_code, 302)
