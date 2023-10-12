"""
Flask server 

This is a Flask API that provides various endpoints for accessing and manipulating data and files.
"""

from flask import Flask
from flask_mysqldb import MySQL
from flask_cors import CORS
from services.config import Config

app = Flask(__name__)
app.app_context()

app.config.from_object(Config)
mysql = MySQL(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

from test import test_routes