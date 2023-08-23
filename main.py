from flask import Flask

from flask_mysqldb import MySQL
from nextcloud import NextCloud
app = Flask(__name__)

nxc = NextCloud(endpoint=NEXTCLOUD_URL, user=NEXTCLOUD_USERNAME, password=NEXTCLOUD_PASSWORD, json_output=to_js)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
