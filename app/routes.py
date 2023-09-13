from app import app,mysql
from flask import request, jsonify
from services.getFiles import create_file_dict

from nextcloud import NextCloud
from dotenv import load_dotenv
load_dotenv()
import os

NEXTCLOUD_URL = os.getenv('NEXTCLOUD_URL')
# my_blueprint = Blueprint('my_blueprint', __name__)
@app.route("/get_data",methods=['POST'])
def fetch_data():
    # mysql = current_app.config['mysql']
    try:
        cursor = mysql.connection.cursor()
        return "Database connection successful! from routes",200
    except Exception as e:
        return f"Database connection failed: {str(e)}",505



@app.route('/getfiles',methods=['POST'])
def get_files_name():
    try:
        json_data = request.json
        username = json_data.get('username')
        password = json_data.get('password')
        if username is None or password is None:
            return jsonify({"error":"username or password is missing"}),404
        
        nxc = NextCloud(endpoint = NEXTCLOUD_URL, user=username, password=password, json_output=True)

        root = nxc.get_folder() 
        file_dict = create_file_dict(root)
        return file_dict
    except:
        return jsonify({"error":"could not get file details"}),500
    


# @app.route('/get_file',methods=['POST'])
# def get_file():
#     json_data = request.json
#     username = json_data.get('username')
#     password = json_data.get('password')
#     filename = json_data.get('filename')
#     if filename is None or username is None or password is None:
#         return 'filename or username or password is missing' 
#     nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=username, password=password, json_output=True)
#     file = nxc.get_file(filename)
#     if file is not None:
#         file.fetch_file_content()
#         file.download()
#         if not check_record_exists(filename):
#             insert_locked_file(username,filename)
#             if scanner(filename):
#                 response = send_file(filename, as_attachment=True)
#                 os.remove(filename)
#                 return response
#             else:
#                 os.remove(filename)
#                 return 'file has virus',505
#         elif check_same_user(username,filename):
#             if scanner(filename):
#                 response = send_file(filename, as_attachment=True)
#                 os.remove(filename)
#                 return response
#             else:
#                 os.remove(filename)
#                 return 'file has virus',505
#         else:
#             os.remove(filename)
#             return 'file already in editing process by another user',404
        
#     else:
#         return 'file not exist or user have not access',404