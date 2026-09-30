from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        file_path = self.path.split('?')[0].lstrip('/')
        if not file_path or file_path == '/':
            file_path = 'index.html'
        if not os.path.exists(file_path):
            file_path = 'index.html'
            
        ext = os.path.splitext(file_path)[1].lower()
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css; charset=utf-8',
            '.js': 'application/javascript; charset=utf-8',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.json': 'application/json',
            '.ico': 'image/x-icon',
        }
        content_type = content_types.get(ext, 'application/octet-stream')
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

def app(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    if not path or path == '/':
        path = 'index.html'
    if not os.path.exists(path):
        path = 'index.html'
    ext = os.path.splitext(path)[1].lower()
    content_types = {
        '.html': 'text/html; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.js': 'application/javascript; charset=utf-8',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.svg': 'image/svg+xml',
        '.json': 'application/json',
        '.ico': 'image/x-icon',
    }
    content_type = content_types.get(ext, 'application/octet-stream')
    try:
        with open(path, 'rb') as f:
            body = f.read()
        status = '200 OK'
        headers = [('Content-Type', content_type), ('Content-Length', str(len(body)))]
        start_response(status, headers)
        return [body]
    except Exception as e:
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain')]
        start_response(status, headers)
        return [str(e).encode('utf-8')]

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), handler)
    print("Serving on http://localhost:8000")
