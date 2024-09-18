import http.server
import socketserver
import os

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        """
        Overriding translate_path to handle both 'index.html' and WASM files.
        """
        # If path is '/', serve 'index.html'
        if path == '/':
            path = '/index.html'

        # Handle WASM files
        if path == '/dugeon.wasm':
            path = '/dugeon.wasm'

        # Handle other static files
        path = super().translate_path(path)
        return path

    def do_GET(self):
        try:
            # Attempt to open the requested file
            with open(self.translate_path(self.path), 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-type', self.guess_type(self.path))
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File Not Found: %s" % self.path)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()