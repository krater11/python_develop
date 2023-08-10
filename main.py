from utils.application import Application
from wsgiref.simple_server import make_server

with make_server("", 8000, Application()) as httpd:
    print("Serving on http://127.0.0.1:8000")

    httpd.serve_forever()