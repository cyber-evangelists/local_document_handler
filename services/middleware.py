from werkzeug.wrappers import Request
from services.cryptography import encrypt_value, decrypt_value
import json
class middleware():
    '''
    middleware
    every request will be passed through this middleware
    '''

    def __init__(self, app):
        self.app = app
        # self.userName = 'Tony'
        # self.password = 'IamIronMan'

    def __call__(self, environ, start_response):
        request = Request(environ)
        excluded_routes = ['/login']
        if request.path in excluded_routes:
            return self.app(environ, start_response)

        request_data_bytes = request.get_data()
        request_data = json.loads(request_data_bytes.decode('utf-8'))
        username_from_json = request_data.get('username')
        password_from_json = request_data.get('password')
        username_from_json = decrypt_value(username_from_json)
        password_from_json = decrypt_value(password_from_json)
        environ['app.username'] = password_from_json
        environ['app.password'] = password_from_json
        return self.app(environ, start_response)
        # if username_from_json == self.userName and password_from_json == self.password:
        #     environ['user'] = { 'name': 'Tony' }

        # res = Response(u'Authorization failed', mimetype= 'text/plain', status=401)
        # return res(environ, start_response)