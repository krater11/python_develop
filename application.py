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
