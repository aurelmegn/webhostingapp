# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
# CSRF_SESSION_KEY = "YMNx&VZ<:85#=61_dUr\x0b*)vL"

WTF_CSRF_CHECK_DEFAULT = False

# Secret key for signing cookies
SECRET_KEY = "YMNx&VZ<:85#=61_dUr\x0b*)vL"

SQLALCHEMY_DATABASE_URI = "sqlite:///./var/data.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://aurel:shift@localhost/clientapp"
SQLALCHEMY_TRACK_MODIFICATIONS = True
WEBPACKEXT_MANIFEST_PATH = "manifest.json"

SERVER_NAME = "localhost:5000"
SECURITY_LOGIN_USER_TEMPLATE = "security/login.jinja"
SECURITY_TRACKABLE = True

SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "YMNx&VZ<:85#=61_dUr\x0b*)vL"
SECURITY_POST_LOGIN_VIEW = "/dashboard"
SECURITY_REGISTERABLE = False
SECURITY_UNAUTHORIZED_VIEW = "/login"

DEBUG_TB_INTERCEPT_REDIRECTS = False

FTP_BASE_DIR = "/media/aurel/main/projects/self/clientapp/tmp"
FTP_PORT = 2121
FTP_HOST = "ftp://localhost"

# FLASK_ADMIN_SWATCH= 'flaty'

from os.path import abspath
SUPERVISOR_CONFIG_DIR = "./supervisor"
SUPERVISOR_USER_HOME = "{supervisor_path}/programs/{username}"
SUPERVISOR_PROGRAM_TEMPLATE_PATH = "./supervisor/subprogram_template.ini"
UWSGI_TEMPLATE_PATH = "./supervisor/uwsgi_template.ini"
FIREJAIL_PROFILE = "./supervisor/default.profile"

ABS_PATH_HOME_UWSGI = "/home/aurel" # should change on production 