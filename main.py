from flask import Flask, request, jsonify

from flask_mysqldb import MySQL
from nextcloud import NextCloud
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

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    global nxc
    nxc = NextCloud(endpoint='http://host.docker.internal:8080/', user=username, password=password, json_output=True)
    # return {'status': 'success'}
    return 'done'

@app.route('/upload_file',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    check = nxc.upload_file('requirements.txt', '/local/requirements.txt').data
    if check:
        return True
    else:
        return False 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
