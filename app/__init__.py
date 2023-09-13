from flask import Flask
"""
Flask server 

This is a Flask API that provides various endpoints for accessing and manipulating data and files.
"""

from flask_mysqldb import MySQL
from flask_cors import CORS
# from services.middleware import middleware
from services.config import Config

app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

from app import routes