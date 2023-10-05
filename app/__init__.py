from flask import Flask
"""
Flask server 

This is a Flask API that provides various endpoints for accessing and manipulating data and files.
"""

from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from services.middleware import middleware
from services.config import Config
from sqlalchemy_utils.functions import database_exists, create_database

app = Flask(__name__)

app.wsgi_app = middleware(app.wsgi_app)
app.config.from_object(Config)
mysql = MySQL(app)
db = SQLAlchemy(app)

# app.config['CORS_HEADERS'] = 'Content-Type'

# @app.after_request
# def after_request(response):
#     print('after request')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     return response
with app.app_context():
    if not database_exists('mysql+pymysql://root:example@localhost:3306/document_handler'):
        create_database('mysql+pymysql://root:example@localhost:3306/document_handler')
    db.create_all()


CORS(app, resources={r"*": {"origins": "*"}})

from app import routes