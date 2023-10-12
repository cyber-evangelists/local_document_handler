from werkzeug.wrappers import Request

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
        
        if request.path in '/get_files_data':
            return self.app(environ, start_response)
        
        if request.path in '/upload_file':
            return self.app(environ, start_response)
