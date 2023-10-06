from flask import Flask

from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from services.middleware import middleware
from services.logs import logger
import os
load_dotenv()

"""
Flask server 

This is a Flask API that provides various endpoints for accessing and manipulating data and files.
"""
MYSQL_URL = os.getenv('MYSQL_URL')

app = Flask(__name__)
app.wsgi_app = middleware(app.wsgi_app)
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app, resources={r"*": {"origins": "*"}})


from app import routes
