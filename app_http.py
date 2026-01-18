from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/health":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html = """
            <html>
            <head><title>News Scanner</title></head>
            <body>
            <h1>✅ News Scanner - LIVE on Railway</h1>
            <p>Time: """ + datetime.now().isoformat() + """</p>
            <p>Server is running!</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"[{datetime.now().isoformat()}] {format % args}")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8501), RequestHandler)
    print("Server starting on 0.0.0.0:8501...")
    server.serve_forever()
