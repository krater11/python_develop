from http.server import ThreadingHTTPServer
from application import Application


def run_server():

    host = '127.0.0.1'
    port = 8000

    server_address = (host, port)
    httpd = ThreadingHTTPServer(server_address, Application)

    print("Serving on http://"+host+":"+str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()