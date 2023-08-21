import cgi
import json
import base64
from utils.GetImageInformation import get_image_information
from utils.GetUrl import get_url_data
from DBManager.AuthToken import BasicAuth
from http.server import BaseHTTPRequestHandler
from DBManager.Permission import permission_status
from DBManager.RichTextInfo import upload_rich_text, get_rich_text, update_rich_text, delete_rich_text
from DBManager.UserInfo import UserRegist, UserLogin
from DBManager.ImageInfo import UploadImage, GetImage, GetImageList, DeleteImage
from DBManager.ManageInfo import ManageLogin, ManageRegist
from DBManager.PermissionManage import get_superuser_status, get_user_permission, manage_permission
from DBManager.TokenAuthorization import token_authorization
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message


class Application(BaseHTTPRequestHandler):
    # 登录检验
    def basic_auth(self):
        try:
            auth_header = self.headers.get('Authorization')
            auth_token = auth_header.split(' ')[-1]
            username_password = base64.b64decode(auth_token).decode('utf-8')
            username, password = username_password.split(':')
            basic_auth_status = BasicAuth(username, password)
            return username, basic_auth_status
        except Exception:
            return "", 400

    def token_auth(self):
        try:
            authorization_header = self.headers.get('Authorization')
            if authorization_header and authorization_header.startswith('Bearer '):
                # 拆分令牌部分
                token = authorization_header.split(' ', 1)[1]
                username, status = token_authorization(token)
            return username, status
        except Exception:
            return "", 400

    def auth(self):
        username1, status1 = self.basic_auth()
        username2, status2 = self.token_auth()
        if status1 == 400 and status2 == 400:
            return "", 400, bad_message("身份验证失败")
        elif status1 == 200 and status2 == 400:
            return username1, 200, normal_good_message("身份验证成功")
        elif status1 == 400 and status2 == 200:
            return username2, 200, normal_good_message("身份验证成功")
        else:
            if username1 == username2:
                return username1, 200, normal_good_message("身份验证成功")
            else:
                return "", 400, bad_message("用户名与Token不匹配，身份验证失败")

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
        elif path[0] == "/api/image_info":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['read_permission'])):
                    try:
                        url = f"http://{self.headers['Host']}{self.path}"
                        imagename = get_url_data(url)['image']
                        response_code, message = GetImage(imagename)
                        if response_code == 200:
                            self.send_response(response_code)
                            self.send_header('Content-type', 'image/jpeg')
                            self.end_headers()
                            for i in message:
                                with open(i, 'rb') as file:
                                    self.wfile.write(file.read())
                        else:
                            bmessage = message.encode("utf-8")
                            self.send_response(response_code)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(bmessage)
                    except Exception:
                        bmessage = "数据格式错误".encode("utf-8")
                        self.send_response(400)
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

        # 图片信息
        elif path[0] == "/api/image_list":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['read_permission'])):
                    try:
                        response_code, message = GetImageList()
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

        # 查看所有用户权限
        elif path[0] == "/api/manage_permission_list":
            username, status, message = self.auth()
            if status == 200:
                if bool(get_superuser_status(username)):
                    try:
                        response_code, message = get_user_permission()
                        bmessage = message.encode("utf-8")
                    except Exception:
                        response_code = 400
                        bmessage = "数据格式错误".encode("utf-8")
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

        # 富文本
        elif path[0] == "/api/rich_text":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['read_permission'])):
                    try:
                        url = f"http://{self.headers['Host']}{self.path}"
                        text_name = get_url_data(url)['text'][0]
                        response_code, message = get_rich_text(text_name)
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

        # 无响应页
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    # POST请求
    def do_POST(self):

        # 管理员注册
        if self.path == "/api/manage_regist":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                response_code, message = ManageRegist(data)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        # 管理员登录
        elif self.path == "/api/manage_login":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                response_code, message = ManageLogin(data)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        # 权限管理
        elif self.path == "/api/manage_permission_list":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                response_code, message = manage_permission(data)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        # 普通用户注册
        elif self.path == "/api/regist":
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                response_code, message = UserRegist(data)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        # 普通用户登录
        elif self.path == "/api/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(post_data)
            response_code, message = UserLogin(data)
            bmessage = message.encode("utf-8")
            # try:
            #
            # except Exception:
            #     response_code = 400
            #     bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        # 上传图片
        elif self.path == "/api/image_info":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['upload_permission'])):
                    try:
                        content_type, _ = cgi.parse_header(self.headers['content-type'])
                        form = cgi.FieldStorage(
                            fp=self.rfile,
                            headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'}
                        )
                        file_field = form['image']
                        imagename, imagefile = get_image_information(file_field)
                        response_code, message = UploadImage(imagefile, imagename)
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

        # 上传富文本
        elif self.path == "/api/rich_text":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['upload_permission'])):
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        data = json.loads(post_data)
                        response_code, message = upload_rich_text(data)
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

        # 无响应页
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    # UPDATE请求
    def do_PUT(self):

        if self.path == "/api/rich_text":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['update_permission'])):
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        data = json.loads(post_data)
                        response_code, message = update_rich_text(data)
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

        # 无响应页
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_DELETE(self):

        # 删除富文本
        if self.path == "/api/rich_text":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['update_permission'])):
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        data = json.loads(post_data)
                        response_code, message = delete_rich_text(data)
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

        # 删除图片
        elif self.path == "/api/image_info":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['update_permission'])):
                    try:
                        content_type, _ = cgi.parse_header(self.headers['content-type'])
                        form = cgi.FieldStorage(
                            fp=self.rfile,
                            headers=self.headers,
                            environ={'REQUEST_METHOD': 'POST'}
                        )
                        image_name = form['image'].value
                        response_code, message = DeleteImage(image_name)
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

        #无响应页
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
