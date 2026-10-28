import http.server
import socketserver
import webbrowser
import os

PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}/index.html"
        print("="*60)
        print(f"🚀 Social CRM Dashboard đang chạy tại: {url}")
        print("Nhấn Ctrl + C để dừng server.")
        print("="*60)
        httpd.serve_forever()

if __name__ == "__main__":
    run()
