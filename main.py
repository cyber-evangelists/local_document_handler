from sqlalchemy_utils.functions import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy
from app import app, db
import os
'''
    This is the main file that will run the flask server
    It will import the app from app/__init__.py
    and run it
'''

MYSQL_URL = os.getenv('MYSQL_URL')

if __name__ == "__main__":
    with app.app_context():
        if not database_exists(MYSQL_URL):
            create_database(MYSQL_URL)
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
