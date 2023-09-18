


# @app.route('/save-logs',methods=['POST'])
# def save_logs():
#     json_data = request.json
#     username = json_data.get('username')
#     description = json_data.get('Description')
#     machine = json_data.get('Machine')
#     filename = json_data.get('filename')
#     if username is None or description is None or machine is None:
#         return 'username or description or machine is missing',404
#     save_logs_in_db(username,machine,description,filename)
#     return 'logs saved successfully',200

# @app.route('/get-logs',methods=['POST'])
# def get_logs():
#     json_data = request.json
#     username = json_data.get('username')
#     machine = json_data.get('Machine')
#     filename = json_data.get('filename')
#     if username is None or machine is None or filename is None:
#         return 'username or machine is missing or filename is missing',404
#     logs = get_logs_from_db(username,machine,filename)
#     if logs is not None:
#         return logs,200
#     else:
#         return 'no logs found',404


from app import app
'''
    This is the main file that will run the flask server
    It will import the app from app/__init__.py
    and run it
'''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
