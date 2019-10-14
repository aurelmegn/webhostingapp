from typing import List

from os.path import abspath, isdir
from os import mkdir, makedirs

import sys

sys.path.append(".")
sys.path.append("../")

from flask_security.utils import verify_password
from pyftpdlib.authorizers import DummyAuthorizer, AuthenticationFailed
from src import app, User, Application


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
        raise AuthenticationFailed()

    def split_username_from_appname(self, username):
        uname_parts = username.split(":")

        if len(uname_parts) != 2:
            raise AuthenticationFailed(self.msg_no_such_user)

        return tuple(uname_parts)

    def add_anonymous(self, homedir, **kwargs):
        raise AuthenticationFailed()

    def remove_user(self, username):
        raise AuthenticationFailed()

    def override_perm(self, username, directory, perm, recursive=False):
        raise AuthenticationFailed()

    def validate_authentication(self, username, password, handler):

        username, appname = self.split_username_from_appname(username)

        with app.app_context():
            user = User.query.filter_by(username=username).first()

            if username == "anonymous":
                raise AuthenticationFailed(self.msg_anon_not_allowed)

            if not user:
                raise AuthenticationFailed(self.msg_no_such_user)
            elif not user.is_active:
                raise AuthenticationFailed()

            if not verify_password(password, user.password):
                raise AuthenticationFailed(self.msg_wrong_password)

            application = Application.query.filter_by(user=user, name=appname).first()

            if not application:
                raise AuthenticationFailed(self.msg_no_such_user)

    def get_home_dir(self, username):

        username, appname = self.split_username_from_appname(username)

        with app.app_context():
            user = User.query.filter_by(username=username).first()
            application = Application.query.filter_by(user=user, name=appname).first()

            content_path = application.get_app_ftp_content_dir()
            print(content_path)
            # if the user ftp directory don't exist create it
            # the dir is like /tmp/username/appame/content/
            if not isdir(content_path):
                makedirs(content_path)

            return content_path

    def has_user(self, username):
        """Whether the username exists in the virtual users table."""
        username, appname = self.split_username_from_appname(username)

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
        user_home_abs = abspath(user_home)
        given_path_abs = abspath(path)

        # user should not delete directory of application

        if given_path_abs.startswith(user_home_abs):

            return self.read_perms + self.write_perms

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
