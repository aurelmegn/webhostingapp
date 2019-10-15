import sys
from unittest import TestCase

from tests.AppTestBase import AppTestBase

from flask_security.utils import hash_password
from ftpserver.AppAuthorizer import (
    AccountNotEnableException,
    AppAuthorizer,
    AuthenticationFailed,
    ShouldNotBeCalledException,
)
from src import User, app, db

sys.path.append(".")
sys.path.append("../")


class TestAppAuthorizer(AppTestBase, TestCase):
    authorizer = AppAuthorizer()

    def test_add_user(self):
        with self.assertRaises(ShouldNotBeCalledException):
            self.authorizer.add_user(None, None, None)

    def test_add_anonymous(self):
        with self.assertRaises(ShouldNotBeCalledException):
            self.authorizer.add_anonymous(None)

    def test_remove_user(self):
        with self.assertRaises(ShouldNotBeCalledException):
            self.authorizer.remove_user(None)

    def test_override_perm(self):
        with self.assertRaises(ShouldNotBeCalledException):
            self.authorizer.override_perm(None, None, None)

    def test_validate_authentication(self):
        with app.app_context():
            with self.assertRaises(AuthenticationFailed):
                self.authorizer.validate_authentication("anonymous", None, None)

            with self.assertRaises(AuthenticationFailed):
                self.authorizer.validate_authentication("unkownuser", "", None)

            user = self.user
            user.active = False

            db.session.add(user)
            db.session.commit()

            with self.assertRaises(AccountNotEnableException):
                self.authorizer.validate_authentication(
                    user.username, self.test_password, None
                )

    def test_get_home_dir(self):
        user = self.user

        from os.path import isdir, join

        udir = join(app.config.get("FTP_BASE_DIR"), user.username)
        # print(udir)
        # print(self.authorizer.get_home_dir(user.username))
        self.assertEqual(
            udir, self.authorizer.get_home_dir(user.username), "Home path is correct"
        )
        # self.assertTrue(isdir(udir), "User dir exist")
        #
        # for application in user.applications:
        #     appdir = join(udir, application.name)
        #     self.assertTrue(isdir(appdir))
