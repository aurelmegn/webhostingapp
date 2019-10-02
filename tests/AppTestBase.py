from flask_security.utils import hash_password

from src import User, app, db


class AppTestBase:
    test_password = "test-password"
    test_username = "test-user"
    user = None

    def setUp(self):

        # create a user
        u: User = User()
        u.username = self.test_username
        u.email = "test@mail.com"
        u.active = True

        with app.app_context():
            u.password = hash_password("test-password")

        db.session.add(u)
        db.session.commit()

        self.user = u

    def tearDown(self):
        db.session.delete(self.user)
        db.session.commit()

        self.user = None

    @staticmethod
    def login(client, username, password):
        return client.post('/login', data=dict(
            email=username,
            password=password
        ), follow_redirects=True)

    @staticmethod
    def logout(client):
        return client.get('/logout', follow_redirects=True)
