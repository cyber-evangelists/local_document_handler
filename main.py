from app import app
'''
    This is the main file that will run the flask server
    It will import the app from app/__init__.py
    and run it
'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
