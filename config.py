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
    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "apikey"
    MAIL_PASSWORD = environ.get("SENDGRID_API_KEY")
    MAIL_DEFAULT_SENDER = environ.get("MAIL_DEFAULT_SENDER")
