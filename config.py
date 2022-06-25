from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    SECRET_KEY = environ.get("SECRET_KEY") or "a_very_complicated_string"
    MONGODB_SETTINGS = {
        "username": environ.get("MONGODB_SETTINGS_USERNAME"),
        "password": environ.get("MONGODB_SETTINGS_PASSWORD"),
        "host": environ.get("MONGODB_SETTINGS_HOST"),
        "db": environ.get("MONGODB_SETTINGS_DB"),
    }
