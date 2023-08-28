from flask import Flask, request, jsonify, send_file

from flask_mysqldb import MySQL
from nextcloud import NextCloud
import os

app = Flask(__name__)

nxc = None

app.config["MYSQL_HOST"] = "mysql-db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "example"
app.config["MYSQL_DB"] = "files_data"

mysql = MySQL(app)


@app.route("/")
def hello_world():
    return "Hello, Docker Compose Flask and MySQL!"


@app.route("/get_data")
def fetch_data():
    try:
        # conn = my_database.connect()
        # conn.close()
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
    username = request.form.get('username')
    password = request.form.get('password')
    if 'file' not in request.files:
        return "No file part"
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    file = request.files['file']
    file.save(file.filename)
    check = nxc.upload_file(file.filename, '/local/'+file.filename).data
    if check=='':
        os.remove(file.filename)
        return 'file uploaded successfully'
    else:
        os.remove(file.filename)
        return 'error while uploading file' 

@app.route('/get_file',methods=['GET'])
def get_file():
    username = request.form.get('username')
    password = request.form.get('password')
    filename = request.form.get('filename')
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    file = nxc.get_file('/local/'+filename)
    file.fetch_file_content()
    file.download()
    response = send_file(filename, as_attachment=True)
    os.remove(filename)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
