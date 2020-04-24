import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """ Set app configuration vars """
    
    # general config
    SECRET_KEY = os.environ.get("TESTING")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")

    # database config
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail server config
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_DEBUG = False
    MAIL_SUPPRESS_SEND = False
