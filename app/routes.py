from app import app,mysql
from flask import request, jsonify, send_file
from services.getFiles import create_file_dict
from services.queries import insert_locked_file,delete_locked_file,check_record_exists,check_same_user
from services.scan import scanner
from nextcloud import NextCloud
from dotenv import load_dotenv
load_dotenv()
import os
root_dir = os.getcwd()
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
    


@app.route('/get_file',methods=['POST'])
def get_file():
    try:
        json_data = request.json
        username = json_data.get('username')
        password = json_data.get('password')
        filename = json_data.get('file_name')
        file_path = json_data.get('file_path')
        if filename is None or username is None or password is None or file_path is None:
            return jsonify({'error':'filename or username or password is missing or file_path is missing'}),404 
        nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=username, password=password, json_output=True)
        file = nxc.get_file(file_path)
        if file is not None:
            file.fetch_file_content()
            file.download()
            current_file_path = os.path.join(root_dir, filename)
            if not check_record_exists(filename,file_path):
                insert_locked_file(username,filename,file_path)
                if scanner(filename):
                    response = send_file(current_file_path, as_attachment=True)
                    os.remove(filename)
                    return response
                else:
                    os.remove(filename)
                    return jsonify({'error':'file has virus'}),500
            elif check_same_user(username,filename,file_path):

                if scanner(filename):
                    response = send_file(current_file_path, as_attachment=True)
                    os.remove(filename)
                    return response
                else:
                    os.remove(filename)
                    return jsonify({'error':'file has virus'}),500
            else:
                os.remove(filename)
                return jsonify({'warning':'file already in editing process by another user'}),404
            
        else:
            return jsonify({'warning':'file not exist or user have not access'}),404
    except:
        return jsonify({'error':'could not get file'}),500
    



@app.route('/upload_file',methods=['POST'])
def upload_file():
    check = None
    username = request.form.get('username')
    password = request.form.get('password')
    if 'file' not in request.files:
        return "No file part",404
    nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=username, password=password, json_output=True)
    file = request.files['file']
    file.save(file.filename)
    if check_record_exists(file.filename):
        delete_locked_file(username,file.filename)
    if scanner(file.filename):
        check = nxc.upload_file(file.filename, '/'+file.filename).data
        os.remove(file.filename)
        if check=='':
            return 'file uploaded successfully',200
        else:
            return 'file upload failed'
    else:
        os.remove(file.filename)
        return 'error while uploading file or file has virus',505