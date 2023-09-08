from flask import Flask, request, jsonify, send_file

from flask_mysqldb import MySQL
from nextcloud import NextCloud
from virus_total_apis import PublicApi
from flask_cors import CORS
import hashlib
import os

app = Flask(__name__)

app.config["MYSQL_HOST"] = "mysql-db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "example"
app.config["MYSQL_DB"] = "file_data"

mysql = MySQL(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def scanner(filename):
    API_KEY = '88858f77a2c07a9d4e9b6b730ea378d1d2c02e3c9e3e9ff885cb1e50da23014b'
    with open(filename, "rb") as file:
        EICAR_MD5 = hashlib.md5(file.read()).hexdigest()

    vt = PublicApi(API_KEY)
    response = vt.get_file_report(EICAR_MD5)
   
    if response["response_code"] == 200:
        return response["results"]["response_code"] == 0 or response["results"]["positives"] == 0
    return False

def insert_locked_file(username,filename):
    cur = mysql.connection.cursor()
    insert_query = "INSERT INTO locked_files (username, file_name, file_url) VALUES (%s, %s, %s)"
    data = (username, filename, '/'+filename)
    cur.execute(insert_query, data)
    mysql.connection.commit()
    cur.close()

def save_logs_in_db(username,machine,descriptoion,filename):
    cur = mysql.connection.cursor()
    insert_query = "INSERT INTO Logging (Description, UserName, Machine,Filename) VALUES (%s, %s, %s, %s)"
    data = (descriptoion, username, machine, filename)
    cur.execute(insert_query, data)
    mysql.connection.commit()
    cur.close()

def get_logs_from_db(username,machine,filename):
    cur = mysql.connection.cursor()
    select_query = """
            SELECT Description
            FROM Logging
            WHERE UserName = %s
              AND Machine = %s
              AND filename = %s
            ORDER BY created_at DESC
            LIMIT 1;
        """
    data = (username, machine, filename)
    cur.execute(select_query, data)
    result = cur.fetchone()
    cur.close()
    if result:
        return result[0]
    else:
        return None

def delete_locked_file(username,filename):
    cur = mysql.connection.cursor()
    delete_query = "DELETE FROM locked_files WHERE username = %s AND file_name = %s"
    data = (username, filename)
    cur.execute(delete_query, data)
    mysql.connection.commit()
    cur.close()

def check_record_exists(file_name):
    cur = mysql.connection.cursor()
    query = "SELECT id FROM locked_files WHERE file_name = %s AND file_url = %s"
    data = (file_name, '/'+file_name)
    cur.execute(query, data)
    result = cur.fetchone()
    cur.close()
    if result:
        return True
    else:
        return False


def check_same_user(username,file_name):
    cur = mysql.connection.cursor()
    query = "SELECT username FROM locked_files WHERE file_name = %s AND file_url = %s"
    data = (file_name, '/'+file_name)
    cur.execute(query, data)
    result = cur.fetchone()
    cur.close()
    if result[0]==username:
        return True
    else:
        return False
    

@app.route("/get_data")
def fetch_data():
    try:
        cursor = mysql.connection.cursor()
        return "Database connection successful!",200
    except Exception as e:
        return f"Database connection failed: {str(e)}",505


@app.route('/getfiles',methods=['POST'])
def get_files_name():
    file_name = []
    json_data = request.json
    username = json_data.get('username')
    password = json_data.get('password')
    if username is None or password is None:
        return 'username or password is missing',404
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    def create_file_dict(folder):
        file_dict = {} 
        def _list_rec(d, current_path=""):
            if d.isdir():
                for i in d.list():
                    new_path = current_path + '/' + i.basename() if current_path else i.basename()
                    _list_rec(i, new_path)
            else:
                file_dict[d.basename()] = current_path

        _list_rec(folder)
        return file_dict

    root = nxc.get_folder() 
    file_dict = create_file_dict(root)
    return file_dict


@app.route('/upload_file',methods=['POST'])
def upload_file():
    check = None
    username = request.form.get('username')
    password = request.form.get('password')
    if 'file' not in request.files:
        return "No file part",404
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
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


@app.route('/get_file',methods=['POST'])
def get_file():
    json_data = request.json
    username = json_data.get('username')
    password = json_data.get('password')
    filename = json_data.get('filename')
    if filename is None or username is None or password is None:
        return 'filename or username or password is missing' 
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    file = nxc.get_file(filename)
    if file is not None:
        file.fetch_file_content()
        file.download()
        if not check_record_exists(filename):
            insert_locked_file(username,filename)
            if scanner(filename):
                response = send_file(filename, as_attachment=True)
                os.remove(filename)
                return response
            else:
                os.remove(filename)
                return 'file has virus',505
        elif check_same_user(username,filename):
            if scanner(filename):
                response = send_file(filename, as_attachment=True)
                os.remove(filename)
                return response
            else:
                os.remove(filename)
                return 'file has virus',505
        else:
            os.remove(filename)
            return 'file already in editing process by another user',404
        
    else:
        return 'file not exist or user have not access',404


@app.route('/login',methods=['POST'])
def login():
    json_data = request.json
    username = json_data.get('username')
    password = json_data.get('password')
    if username is None or password is None:
        return 'username or password or machine is missing or ip is missing'
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    check = nxc.upload_file('checklogin.txt', '/flask/checklogin.txt').data
    if check=='':
        return jsonify({'status':'login sucessfull'}),200
    else:
        return jsonify({'status':'login failed'}),401
    

@app.route('/save-logs',methods=['POST'])
def save_logs():
    json_data = request.json
    username = json_data.get('username')
    description = json_data.get('Description')
    machine = json_data.get('Machine')
    filename = json_data.get('filename')
    if username is None or description is None or machine is None:
        return 'username or description or machine is missing',404
    save_logs_in_db(username,machine,description,filename)
    return 'logs saved successfully',200

@app.route('/get-logs',methods=['POST'])
def get_logs():
    json_data = request.json
    username = json_data.get('username')
    machine = json_data.get('Machine')
    filename = json_data.get('filename')
    if username is None or machine is None or filename is None:
        return 'username or machine is missing or filename is missing',404
    logs = get_logs_from_db(username,machine,filename)
    if logs is not None:
        return logs,200
    else:
        return 'no logs found',404
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
