from http.server import ThreadingHTTPServer
from application import Application
from utils.GenerateRequirements import generate_requirements
from settings import PORT, HOST


def run_server():
    server_address = (HOST, PORT)
    httpd = ThreadingHTTPServer(server_address, Application)

    print("Serving on http://" + HOST + ":" + str(PORT))
    httpd.serve_forever()


if __name__ == "__main__":
    generate_requirements()
    run_server()
