from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Hello from Python HTTP Server!</h1>')
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("Received POST data:", post_data.decode())
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'POST received')

# Запуск сервера
server = HTTPServer(('localhost', 8000), SimpleHandler)
print("Server started on http://localhost:8000")
server.serve_forever()