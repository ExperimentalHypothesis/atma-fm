import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    STREAM_SERVER_BASE_URL = os.environ.get("STREAM_SERVER_BASE_URL", "http://localhost:8000")

