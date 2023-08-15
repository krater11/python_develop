import base64
from DBManager.AuthToken import BasicAuth
from DBManager.UserInfo import UserRegist, UserLogin
from DBManager.ImageInfo import UploadImage,GetImage
from http.server import BaseHTTPRequestHandler
import json
from DBManager.Permission import permission_status
from utils.GetUrl import get_url_data
from utils.GetFile import get_file_filename
from DBManager.ManageInfo import ManageLogin,ManageRegist
from DBManager.PermissionManage import get_superuser_status, get_user_permission, manage_permission


class Application(BaseHTTPRequestHandler):
    # 登录检验
    def basic_auth(self):
        auth_header = self.headers.get('Authorization')

        auth_token = auth_header.split(' ')[-1]
        username_password = base64.b64decode(auth_token).decode('utf-8')
        username, password = username_password.split(':')
        basic_auth_status, message = BasicAuth(username, password)
        return username, basic_auth_status, message

    # GET请求
    def do_GET(self):
        path = self.path.split("?")
        # 主页
        if path[0] == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Welcome Home")
        # 获取照片
        elif path[0] == "/api/get_image":
            username, status, message = self.basic_auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['read_permission'])):
                    url = f"http://{self.headers['Host']}{self.path}"
                    image_name = get_url_data(url)['image'][0]
                    response_code, message = GetImage(image_name)
                    self.send_response(response_code)
                    self.send_header('Content-type', 'image/jepg')
                    self.end_headers()
                    with open(message, 'rb') as file:
                        self.wfile.write(file.read())
                else:
                    bmessage = "用户缺少权限".encode("utf-8")
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bmessage)
            else:
                bmessage = message.encode("utf-8")
                self.send_response(status)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bmessage)
        # 查看所有用户权限
        elif path[0] == "/api/manage_permission_list":
            username, status, message = self.basic_auth()
            if status == 200:
                if bool(get_superuser_status(username)):
                    response_code, message = get_user_permission()
                    bmessage = message.encode("utf-8")
                    self.send_response(response_code)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bmessage)
                else:
                    bmessage = "非管理员用户缺少权限".encode("utf-8")
                    self.send_response(400)
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

    #POST请求
    def do_POST(self):

        if self.path == "/api/manage_regist":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                username = data["user_name"]
                userpassword = data["user_password"]
                userphone = data["user_phone"]
                response_code, message = ManageRegist(username, userpassword, userphone)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/manage_login":
            try:
                auth_header = self.headers.get('Authorization')
                auth_token = auth_header.split(' ')[-1]
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                username = data["user_name"]
                userpassword = data["user_password"]
                response_code, message = ManageLogin(username, userpassword, auth_token)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/manage_permission_list":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            username = data["user_name"]
            upload_permission = data["upload_permission"]
            read_permission = data["read_permission"]
            update_permission = data["update_permission"]
            permission_data = [upload_permission, read_permission, update_permission]
            response_code, message = manage_permission(username, permission_data)
            bmessage = message.encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/regist":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                username = data["user_name"]
                userpassword = data["user_password"]
                userphone = data["user_phone"]
                response_code, message = UserRegist(username, userpassword, userphone)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/login":
            try:
                auth_header = self.headers.get('Authorization')
                auth_token = auth_header.split(' ')[-1]
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                username = data["user_name"]
                userpassword = data["user_password"]
                response_code, message = UserLogin(username, userpassword, auth_token)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/upload_image":
            username, status, message = self.basic_auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['upload_permission'])):
                    try:
                        content_type = self.headers['Content-Type']
                        content_length = int(self.headers['Content-Length'])
                        data = self.rfile.read(content_length)
                        image_file, image_name = get_file_filename(content_type, data)
                        response_code, message = UploadImage(image_file, image_name)
                        bmessage = message.encode("utf-8")
                    except Exception:
                        response_code = 400
                        bmessage = "数据格式错误".encode("utf-8")
                    self.send_response(response_code)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(bmessage)
                else:
                    bmessage = "用户缺少权限".encode("utf-8")
                    self.send_response(400)
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

