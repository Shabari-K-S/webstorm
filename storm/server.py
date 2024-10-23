import os
import socket
import mimetypes
import webbrowser

from .request import HTTPRequest

class TCPServer:
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.host = host
        self.port = port
    
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"Server started on {self.host}:{self.port}")
        print("Press Ctrl+C to stop the server")
        webbrowser.open(f"http://{self.host}:{self.port}")
        while True:
            client_socket, client_address = s.accept()
            print(f"Connected by {client_address}")
            
            data = client_socket.recv(1024)
            response = self.handle_request(data)
            client_socket.sendall(response)
            client_socket.close()

    def handle_request(self, data: bytes) -> bytes:
        return data

class HTTPServer(TCPServer):
    headers = {
        'Server': 'Storm/0.0.1',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: "200 OK",
        404: "404 Not Found",
        501: "501 Not Implemented",
    }
    
    def handle_request(self, data: bytes) -> bytes:
        request = HTTPRequest(data)

        try:
            handler = getattr(self, 'handle_%s' % request.method)
        except AttributeError:
            handler = self.HTTP_501_handler
        
        response = handler(request)
        return response

    def response_line(self, status_code: int) -> bytes:
        reason = self.status_codes[status_code]
        return f'HTTP/1.1 {status_code} {reason}\r\n'.encode()

    def response_headers(self, extra_headers: dict = None) -> bytes:
        headers_copy = self.headers.copy()

        if extra_headers:
            headers_copy.update(extra_headers)
        
        headers = ''.join([f'{key}: {value}\r\n' for key, value in headers_copy.items()])
        return headers.encode()

    def handle_OPTIONS(self, request) -> bytes:
        response_line = self.response_line(200)
        extra_headers = {'Allow': 'OPTIONS, GET'}
        response_headers = self.response_headers(extra_headers)
        blank_line = b'\r\n'

        return b''.join([response_line, response_headers, blank_line])

    def handle_GET(self, request) -> bytes:
        path = request.uri

        if path in self.routes:
            handler = self.routes[path]
            response_body = handler()
            if isinstance(response_body, str):
                response_body = response_body.encode()
            response_line = self.response_line(200)
            self.headers['Content-Type'] = 'text/html'
        else:
            # Assets and template paths come from user-specified directories
            if path.startswith('/assets/'):
                file_path = os.path.join(self.assets_dir, path[8:])  # Skip '/assets/' in path
            else:
                file_path = os.path.join(self.static_dir, path)
            
            if os.path.exists(file_path) and not os.path.isdir(file_path):
                with open(file_path, 'rb') as f:
                    response_body = f.read()
                response_line = self.response_line(200)
                content_type, _ = mimetypes.guess_type(file_path)
                if content_type:
                    self.headers['Content-Type'] = content_type
            else:
                response_line = self.response_line(404)
                response_body = b'<h1>404 Not Found</h1>'
                self.headers['Content-Type'] = 'text/html'

        self.headers['Content-Length'] = str(len(response_body))
        response_headers = self.response_headers()
        
        return b''.join([response_line, response_headers, b'\r\n', response_body])

    def HTTP_501_handler(self, request) -> bytes:
        response_line = self.response_line(501)
        response_headers = self.response_headers()
        response_body = b'<h1>501 Not Implemented</h1>'

        return b''.join([response_line, response_headers, b'\r\n', response_body])

class Storm(HTTPServer):
    def __init__(self, host: str = 'localhost', port: int = 8080, static_dir: str = 'static', assets_dir: str = 'assets'):
        super().__init__(host, port)
        self.routes = {}
        self.static_dir = static_dir  # User-defined static directory
        self.assets_dir = assets_dir  # User-defined assets directory

    def route(self, path):
        def decorator(f):
            self.routes[path] = f
            return f
        return decorator
    
    def start(self):
        try:
            super().start()
        except KeyboardInterrupt:
            print("Server stopped")
