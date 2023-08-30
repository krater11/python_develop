import os
import cgi
import json
import base64
import socket
import tempfile
from DBManager.Advertisement import upload_ad, get_ad_information, delete_ad_information, update_ad_information
from DBManager.File import upload_file, delete_file
from settings import ROOT_PATH
from utils.GetFileInformation import get_file_information
from utils.GetUrl import get_url_data
from DBManager.AuthToken import BasicAuth
from http.server import BaseHTTPRequestHandler
from DBManager.Permission import permission_status
from DBManager.RichTextInfo import upload_rich_text, get_rich_text, update_rich_text, delete_rich_text
from DBManager.UserInfo import UserRegist, UserLogin
from DBManager.ManageInfo import ManageLogin, ManageRegist
from DBManager.PermissionManage import get_superuser_status, get_user_permission, manage_permission
from DBManager.TokenAuthorization import token_authorization
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message
from DBManager.WebInformation import upload_webinformation, get_web_information
from utils.ContentType import content_type


class Application(BaseHTTPRequestHandler):

    # 用户民密码检验
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

    # Token验证
    def token_auth(self):

        try:
            authorization_header = self.headers.get('Authorization')
            token = authorization_header[1:-1]
            username, status = token_authorization(token)
            return username, status
        except Exception:
            return "", 400

    # 身份验证
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
            self.wfile.write("home".encode("utf-8"))

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
                        rich_text_type = get_url_data(url)['type'][0]
                        response_code, message = get_rich_text(rich_text_type)
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

        elif path[0] == "/api/web_information":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['read_permission'])):
                    try:
                        response_code, message = get_web_information()
                        bmessage = message.encode("utf-8")
                        self.send_response(response_code)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(bmessage)
                    except Exception:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write("数据格式错误".encode("utf-8"))
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

        elif path[0] == "/api/ad_information":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['read_permission'])):
                    try:
                        url = f"http://{self.headers['Host']}{self.path}"
                        type_class = get_url_data(url)['type'][0]
                        response_code, message = get_ad_information(type_class)
                        bmessage = message.encode("utf-8")
                        self.send_response(response_code)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(bmessage)
                    except Exception:
                        self.send_response(400)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write("数据格式错误".encode("utf-8"))
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
            dir_path = path[0].split(".")[0].split("/")
            if dir_path[1] == "media":
                contenttype = content_type(path[0].split(".")[1])
                root_path = ROOT_PATH.replace("\\", "/")
                static_path = "/".join(path[0].split("/")[:-1])
                try:
                    with open(root_path + path[0], 'rb') as file:
                        data = file.read()
                    with tempfile.NamedTemporaryFile(delete=True, dir=root_path + static_path + "/") as temp_file:
                        temp_file.write(data)
                        temp_file.flush()
                        temp_file.seek(0)
                        file_dat = temp_file.read()
                        self.send_response(200)
                        self.send_header('Content-type', f"{contenttype}")
                        self.end_headers()
                        self.wfile.write(file_dat)
                except Exception:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"404 NOT FOUND")
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"404 NOT FOUND")

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
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(post_data)
                response_code, message = UserLogin(data)
                bmessage = message.encode("utf-8")
            except Exception:
                response_code = 400
                bmessage = "数据格式错误".encode("utf-8")
            self.send_response(response_code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bmessage)

        elif self.path == "/api/file":
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
                        file_field = form['file']
                        filename, file = get_file_information(file_field)
                        response_code, message = upload_file(filename, file)
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
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode("utf-8")
                    data = json.loads(post_data)
                    response_code, message = upload_rich_text(data)
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

        # 上传网站信息
        elif self.path == "/api/web_information":
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
                        file_field = form['file']
                        data = eval(form["text"].value)
                        _, imagefile = get_file_information(file_field)
                        if file_field.value == "":
                            imagefile = [None]
                        response_code, message = upload_webinformation(imagefile, data)
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

        elif self.path == "/api/ad_information":
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
                        file_field = form['file']
                        data = eval(form["text"].value)
                        imagename, imagefile = get_file_information(file_field)
                        if len(imagename) > 1:
                            self.send_response(400)
                            self.send_header('Content-type', 'text/html')
                            self.end_headers()
                            self.wfile.write(bad_message("数据格式错误"))
                        else:
                            response_code, message = upload_ad(imagename[0], imagefile[0], data)
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
            self.wfile.write(b"404 NOT FOUND")

    # UPDATE请求
    def do_PUT(self):

        # 富文本修改
        if self.path == "/api/rich_text":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['update_permission'])):
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode("utf-8")
                    data = json.loads(post_data)
                    response_code, message = update_rich_text(data)
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

        # 广告修改
        elif self.path == "/api/ad_information":
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
                        file_field = form['file']
                        data = eval(form["text"].value)
                        if file_field.value == "" or file_field.value == "null":
                            response_code, message = update_ad_information("", "", data)
                            bmessage = message.encode("utf-8")
                        else:
                            imagename, imagefile = get_file_information(file_field)
                            if len(imagename) > 1:
                                self.send_response(400)
                                self.send_header('Content-type', 'text/html')
                                self.end_headers()
                                self.wfile.write(bad_message("数据格式错误"))
                            else:
                                response_code, message = update_ad_information(imagename[0], imagefile[0], data)
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

        # 删除广告
        elif self.path == "/api/ad_information":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['update_permission'])):
                    try:
                        content_length = int(self.headers['Content-Length'])
                        post_data = self.rfile.read(content_length).decode("utf-8")
                        response_code, message = delete_ad_information(post_data)
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

        elif self.path == "/api/image":
            username, status, message = self.auth()
            if status == 200:
                data = permission_status(username)
                if bool(int(data['update_permission'])):
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode("utf-8")
                    data = json.loads(post_data)
                    response_code, message = delete_file(data)
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
