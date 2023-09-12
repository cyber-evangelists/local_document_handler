from app import app,mysql


@app.route("/get_data",methods=['POST'])
def fetch_data():
    try:
        cursor = mysql.connection.cursor()
        return "Database connection successful! from routes",200
    except Exception as e:
        return f"Database connection failed: {str(e)}",505

