from flask import Flask, request, jsonify, send_file

from flask_mysqldb import MySQL
from nextcloud import NextCloud
from flask_cors import CORS
from services.scan import scanner
from services.middleware import middleware
from services.config import Config
# from .routes import my_blueprint



app = Flask(__name__)



app.config.from_object(Config)
mysql = MySQL(app)

# def init_mysql(app):
# mysql.init_app(app)
# app.register_blueprint(my_blueprint)
# init_mysql(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

from app import routes