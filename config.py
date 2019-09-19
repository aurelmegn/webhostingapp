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
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "YMNx&VZ<:85#=61_dUr\x0b*)vL"

SQLALCHEMY_DATABASE_URI = "sqlite:///./var/data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = True
WEBPACKEXT_MANIFEST_PATH = "manifest.json"

SECURITY_LOGIN_USER_TEMPLATE = "security/login.jinja"
SECURITY_TRACKABLE = True

SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "YMNx&VZ<:85#=61_dUr\x0b*)vL"
