from werkzeug.wrappers import Request
from services.cryptography import decrypt_value
from pathvalidate import sanitize_filename, sanitize_filepath
from flask import abort
import logging
import json
from pprint import pprint


class middleware():
    '''
    middleware
    every request will be passed through this middleware
    '''

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        excluded_routes = ['/login']
        if request.path in excluded_routes:
            return self.app(environ, start_response)

        if request.path in '/get_file':
            return self.app(environ, start_response)
            # try:
            #     request_data_bytes = request.get_data()
            #     # if request_data_bytes is None:
            #     #     return abort(400, 'Bad Request: Request body is empty')
                                    
            #     request_data = json.loads(request_data_bytes.decode('utf-8'))
            #     username_from_json = request_data.get('username')
            #     password_from_json = request_data.get('password')
            #     environ['app.username'] = decrypt_value(username_from_json)
            #     environ['app.password'] = decrypt_value(password_from_json)
            #     environ['app.file_name'] = sanitize_filename(request_data['file_name'])
            #     environ['app.file_path'] = sanitize_filepath(request_data['file_path'])
            #     return self.app(environ, start_response)
            # except Exception as e:
            #     logging.error(e)
            #     return abort(400, f'Bad Request:{e}')
        
        if request.path in '/get_files_data':
            return self.app(environ, start_response)
            # request.headers['Access-Control-Allow-Origin'] = '*'
            # logging.error('aasdasdasdasdasd', request.get_json())
            # if request.get_data():
            #     return abort(400, 'Bad Request: Request body is empty')
            # print(request.json)
            # logging.error("error",request.items())
            # print('username:',request_data_bytes)

            # request_data_bytes = request.get_data()
            # logging.error("asdasd", request_data_bytes)
            # logging.error('headers: ', request.headers)

            
            # logging.error(dir(request))
          
            # request_data_raw = request_data_bytes.decode('utf-8')
            # request_data = json.loads(request_data_raw)
            # username_from_json = request_data.get('username')
            # password_from_json = request_data.get('password')
            # environ['app.username'] = decrypt_value(username_from_json)
            # environ['app.password'] = decrypt_value(password_from_json)
            # return self.app(environ, start_response)
        
        if request.path in '/upload_file':
            return self.app(environ, start_response)
