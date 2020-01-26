from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


# Flask instance
ki = Flask(__name__)
ki.config.from_object(Config)

# Flask SQLAlchemy instance and db init
db = SQLAlchemy(ki)
from ki.models import *
db.create_all()

# Import views
from ki.views import *
