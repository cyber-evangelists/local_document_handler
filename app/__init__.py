from flask import Flask, request, jsonify, send_file

from flask_mysqldb import MySQL
from nextcloud import NextCloud
from flask_cors import CORS
from services.scan import scanner
from services.middleware import middleware
from services.config import Config
from .routes import my_blueprint
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# app.wsgi_app = middleware(app.wsgi_app)

# app.config["MYSQL_HOST"] = "mysql-db"
# app.config["MYSQL_USER"] = "root"
# app.config["MYSQL_PASSWORD"] = "example"
# app.config["MYSQL_DB"] = "file_data"


app.config.from_object(Config)
app.register_blueprint(my_blueprint)

mysql = MySQL(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})