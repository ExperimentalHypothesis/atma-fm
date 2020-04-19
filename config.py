import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """ Set app configuration vars """
    
    # general config
    SECRET_KEY = os.environ.get("TESTING")
    TESTING = os.environ.get("TESTING")
    DEBUG = os.environ.get("DEBUG")
    ENV = os.environ.get("ENV")

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
