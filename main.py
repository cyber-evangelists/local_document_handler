from flask import Flask, request, jsonify, send_file

from flask_mysqldb import MySQL
from nextcloud import NextCloud
from virus_total_apis import PublicApi
import hashlib
import os

app = Flask(__name__)

nxc = None

app.config["MYSQL_HOST"] = "mysql-db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "example"
app.config["MYSQL_DB"] = "files_data"

mysql = MySQL(app)

def scanner(filename):
    API_KEY = '88858f77a2c07a9d4e9b6b730ea378d1d2c02e3c9e3e9ff885cb1e50da23014b'
    with open(filename, "rb") as file:
        EICAR_MD5 = hashlib.md5(file.read()).hexdigest()

    vt = PublicApi(API_KEY)
    response = vt.get_file_report(EICAR_MD5)
   
    if response["response_code"] == 200:
        return response["results"]["response_code"] == 0 or response["results"]["positives"] == 0
    return False


@app.route("/get_data")
def fetch_data():
    try:
        cursor = mysql.connection.cursor()
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"


@app.route('/getfiles',methods=['POST'])
def get_files_name():
    file_name = []
    username = request.form.get('username')
    password = request.form.get('password')
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    root = nxc.get_folder('/local/')  # get root
    def _list_rec(d, indent=""):
        formatted_string = "%s%s" % (d.basename(), '/' if d.isdir() else '')
        if '/' not in formatted_string:
            file_name.append(formatted_string)
        print("%s%s%s" % (indent, d.basename(), '/' if d.isdir() else ''))
        if d.isdir():
            for i in d.list():
                _list_rec(i, indent=indent+"  ")

    _list_rec(root)
    return file_name


@app.route('/upload_file',methods=['POST'])
def upload_file():
    check = None
    username = request.form.get('username')
    password = request.form.get('password')
    if 'file' not in request.files:
        return "No file part"
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    file = request.files['file']
    file.save(file.filename)
    if scanner(file.filename):
        check = nxc.upload_file(file.filename, '/local/'+file.filename).data
        os.remove(file.filename)
        if check=='':
            return 'file uploaded successfully'
        else:
            return 'file upload failed'
    else:
        os.remove(file.filename)
        return 'error while uploading file or file has virus' 


@app.route('/get_file',methods=['GET'])
def get_file():
    username = request.form.get('username')
    password = request.form.get('password')
    filename = request.form.get('filename')
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    file = nxc.get_file('/local/'+filename)
    file.fetch_file_content()
    file.download()
    if scanner(filename):
        response = send_file(filename, as_attachment=True)
        os.remove(filename)
        return response
    else:
        os.remove(filename)
        return 'file has virus'


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
