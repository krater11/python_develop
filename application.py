from DBManager.UserInfo import UserRegist, UserLogin
from DBManager.ImageInfo import UploadImage
from http.server import BaseHTTPRequestHandler
import json
import cgi


class Application(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Welcome Home")

    def do_POST(self):

        if self.path == "/api/regist":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            username = data["user_name"]
            userpassword = data["user_password"]
            userphone = data["user_phone"]
            response_code, message = UserRegist(username, userpassword, userphone)
            bmessage = message.encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        if self.path == "/api/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            username = data["user_name"]
            userpassword = data["user_password"]
            response_code, message = UserLogin(username, userpassword)
            bmessage = message.encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        if self.path == "/api/image_upload":
            content_type, _ = cgi.parse_header(self.headers.get('content-type'))
            form_data = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST'}
            )
            image_file = form_data['image'].value
            image_name = form_data['image']
            print(type(image_name))
            # response_code, message = UploadImage(image_file, image_name)
            # bmessage = message.encode("utf-8")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"message")
