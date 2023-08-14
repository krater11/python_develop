import base64
import os
from DBManager.AuthToken import BasicAuth
from DBManager.UserInfo import UserRegist, UserLogin
from DBManager.ImageInfo import UploadImage,GetImage
from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
import cgi
import tempfile


class Application(BaseHTTPRequestHandler):

    def basic_auth(self):
        auth_header = self.headers.get('Authorization')

        auth_token = auth_header.split(' ')[-1]
        username_password = base64.b64decode(auth_token).decode('utf-8')
        username, password = username_password.split(':')
        basic_auth_status, message = BasicAuth(username, password)
        return basic_auth_status, message

    def do_GET(self):
        path = self.path.split("?")
        if path[0] == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Welcome Home")

        elif path[0] == "/api/get_image":
            status, message = self.basic_auth()
            if status == 200:
                url = f"http://{self.headers['Host']}{self.path}"
                parsed_url = urlparse(url)
                query_params = parse_qs(parsed_url.query)
                image_name = query_params['image'][0]
                response_code, message = GetImage(image_name)
                self.send_response(response_code)
                self.send_header('Content-type', 'image/jepg')
                self.end_headers()
                with open(message, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                bmessage = message.encode("utf-8")
                self.send_response(status)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bmessage)

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

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

        elif self.path == "/api/login":
            auth_header = self.headers.get('Authorization')
            auth_token = auth_header.split(' ')[-1]
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            username = data["user_name"]
            userpassword = data["user_password"]
            response_code, message = UserLogin(username, userpassword,auth_token)
            bmessage = message.encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/image_upload":
            status, message = self.basic_auth()
            if status == 200:
                content_type = self.headers['Content-Type']
                boundary = content_type.split('; ')[1].split('=')[1]

                # 读取请求体的数据
                content_length = int(self.headers['Content-Length'])
                data = self.rfile.read(content_length)

                # 分割数据，找到文件名
                parts = data.split(b'--' + boundary.encode())
                for part in parts:
                    if b'filename=' in part:
                        # 获取文件名
                        filename_start = part.find(b'filename=')
                        filename_end = part.find(b'\r\n', filename_start)
                        image_name = part[filename_start + 10:filename_end - 1].decode()
                        content_start = part.find(b'\r\n\r\n')
                        image_file = part[content_start + 4:-2]

                response_code, message = UploadImage(image_file, image_name)
                bmessage = message.encode("utf-8")

                self.send_response(response_code)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bmessage)
            else:
                bmessage = message.encode("utf-8")
                self.send_response(status)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bmessage)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

