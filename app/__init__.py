from flask import Flask
from config import Config

announcements_app = Flask(__name__)
announcements_app.config.from_object(Config)
from app import routes
