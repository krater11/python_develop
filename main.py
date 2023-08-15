from http.server import ThreadingHTTPServer
from application import Application
from utils.GenerateRequirements import generate_requirements


def run_server():

    host = '127.0.0.1'
    port = 8000

    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, Application)

    print("Serving on http://"+host+":"+str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    generate_requirements()
    run_server()

