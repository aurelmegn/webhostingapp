from typing import List, Union

import os
import sys

sys.path.append(".")
sys.path.append("../")

from flask_security.utils import verify_password
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import DTPHandler
from src import app, User


class AppAuthorizer(DummyAuthorizer):
    def __init__(self):
        self.msg_no_such_user = "Authentication failed."
        self.msg_wrong_password = "Authentication failed."
        self.msg_anon_not_allowed = "Anonymous access not allowed."

    def add_user(
        self,
        username,
        password,
        homedir,
        perm="elr",
        msg_login="Login successful.",
        msg_quit="Goodbye.",
    ):
        # todo throw an error
        pass

    def add_anonymous(self, homedir, **kwargs):
        # todo throw an error

        pass

    def remove_user(self, username):
        # todo throw an error

        pass

    def override_perm(self, username, directory, perm, recursive=False):
        pass

    def validate_authentication(self, username, password, handler):
        with app.app_context():
            user = User.query.filter_by(username=username).first()

            if username == "anonymous":
                raise AuthenticationFailed(self.msg_anon_not_allowed)

            if not user:
                raise AuthenticationFailed(self.msg_no_such_user)

            if not verify_password(password, user.password):
                raise AuthenticationFailed(self.msg_wrong_password)

    def get_home_dir(self, username):

        with app.app_context():
            user = User.query.filter_by(username=username).first()

            base_path = app.config.get('FTP_BASE_DIR')
            home_path = base_path + user.username

            # if the user ftp directory don't exist create it
            if not os.path.isdir(home_path):
                os.mkdir(home_path)

            applications_paths: List[str] = [
                os.path.abspath(os.path.join(home_path, a.name))
                for a in user.applications
            ]
            # create the directories of the application of the user
            for application_path in applications_paths:
                if not os.path.isdir(application_path):
                    os.mkdir(os.path.join(application_path))

            return home_path

    def has_user(self, username):
        """Whether the username exists in the virtual users table."""
        user_count = User.query.filter_by(username=username).count()
        if user_count != 1:
            return False
        return True

    def has_perm(self, username, perm, path=None):
        """Whether the user has permission over path (an absolute
        pathname of a file or a directory).

        Read permissions:
         - "e" = change directory (CWD command)
         - "l" = list files (LIST, NLST, MLSD commands)
         - "r" = retrieve file from the server (RETR command)

        Write permissions:
         - "a" = append data to an existing file (APPE command)
         - "d" = delete file or directory (DELE, RMD commands)
         - "f" = rename file or directory (RNFR, RNTO commands)
         - "m" = create directory (MKD command)
         - "w" = store a file to the server (STOR, STOU commands)
        """

        user_home = self.get_home_dir(username)
        user_home_abs = os.path.abspath(user_home)
        given_path_abs = os.path.abspath(path)

        # user should not delete directory of application

        if given_path_abs.startswith(user_home_abs):
            """if the given path start with the current user home path, check if it is an application directory path"""
            with app.app_context():
                user = User.query.filter_by(username=username).first()

                applications_paths = [
                    os.path.abspath(os.path.join(user_home, a.name))
                    for a in user.applications
                ]
                if given_path_abs in applications_paths:
                    return "elrafmwMT"

                return "elrafdmwMT"

        return ""

    def get_perms(self, username):
        """Return current user permissions."""
        return "elradfmwMT"

    def get_msg_login(self, username):
        """Return the user's login message."""

        return f"Welcome {username}."

    def get_msg_quit(self, username):
        """Return the user's quitting message."""

        return f"Goodbye {username}."


# ===================================================================
# --- exceptions
# ===================================================================


class AuthorizerError(Exception):
    """Base class for authorizer exceptions."""


class AuthenticationFailed(Exception):
    """Exception raised when authentication fails for any reason."""
