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

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
with open (os.path.join("app", "aws-key.pem"), "r") as myfile:
    secret_key = myfile.read()
SECRET_KEY = "secret"

SECRET_KEY=secret_key
WTF_CSRF_SECRET_KEY="a csrf secret key"

SQLALCHEMY_DATABASE_URI='postgresql://localhost/cbdblocal'

DEBUG=True

if "PRODUCTION" in os.environ:
    SQLALCHEMY_DATABASE_URI='postgresql://dre:disruption@aa3gb6uniecu4v.cjvamjemslrm.us-west-1.rds.amazonaws.com:5432/ebdb'
