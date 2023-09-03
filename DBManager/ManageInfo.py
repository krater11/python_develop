import json
import sqlite3

from DBManager.DBConnect import connectdb
from utils.HashNumber import hash_string
from settings import DATABASE, RESPONSE_GOOD_MESSAGE, RESPONSE_BAD_MESSAGE
from datetime import datetime
from utils.IFSuperUser import if_superuser
from utils.GenerateToken import generate_token
from utils.ResponseGoodMessage import login_good_message, normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message
from utils.IfTime import if_expire_time
from utils.AddTime import add_time


def ManageRegist(data):
    try:
        conn, c = connectdb()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS UserInfo (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name VARCHAR UNIQUE,
        user_password VARCHAR,
        user_phone INTEGER (11),
        user_createtime DATETIME,
        user_token VARCHAR (255),
        superuser INTEGER)''')
    except Exception:
        return 400, bad_message("数据库连接失败")


    username = data["user_name"]
    userpassword = data["user_password"]
    userphone = data["user_phone"]
    item = c.execute("SELECT user_name FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()

    if useritem is not None:
        conn.close()
        return 400, bad_message("用户名已存在")

    hashuserpassword = hash_string(userpassword)
    createtime = datetime.now()
    usercreatetime = createtime.strftime("%Y-%m-%d %H:%M:%S")
    data = (username, hashuserpassword, userphone, usercreatetime, 1)
    c.execute(
        "INSERT INTO UserInfo (user_name, user_password, user_phone, user_createtime, superuser) VALUES(?, ?, ?, ?, ?)",
        data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("注册成功")


def ManageLogin(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    username = data["user_name"]
    userpassword = data["user_password"]
    hashpassword = hash_string(userpassword)

    useritem = c.execute("SELECT user_password FROM UserInfo WHERE user_name = '%s'" % username).fetchone()
    if useritem is None:
        conn.close()
        return 400, bad_message("用户不存在")
    if not hashpassword == useritem[0]:
        conn.close()
        return 400, bad_message("密码错误")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS PermissionInfo (
    user_id INTEGER REFERENCES UserInfo (user_id),
    upload_permission VARCHAR,
    read_permission VARCHAR,
    update_permission VARCHAR)''')

    if not if_superuser(username):
        conn.close()
        return 400, bad_message("非管理员用户")

    user_id = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]
    if c.execute("SELECT user_id FROM PermissionInfo WHERE user_id = '%d'" % user_id).fetchone() is None:
        c.execute(
            "INSERT INTO PermissionInfo (user_id, upload_permission, read_permission, update_permission) VALUES(? ,?, ?, ?)",
            (user_id, 1, 1, 1))
        conn.commit()

    auth_token = generate_token(username, userpassword)
    user_item = c.execute("SELECT user_token FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]
    if user_item is not None:
        token_expire_time = c.execute("SELECT token_expire_time FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]
        if if_expire_time(token_expire_time):
            auth_token = generate_token(username, userpassword)
            token_expire_time = add_time()
            c.execute("UPDATE UserInfo SET user_token = ?, token_expire_time = ? WHERE user_name = ?", (auth_token, token_expire_time, username))
            conn.commit()
            conn.close()
            return 200, login_good_message("登录成功", auth_token)
        else:
            conn.close()
            return 200, login_good_message("登录成功", user_item)
    token_expire_time = add_time()
    c.execute("UPDATE UserInfo SET user_token = ?, token_expire_time = ? WHERE user_name = ?", (auth_token, token_expire_time, username))

    conn.commit()
    conn.close()
    return 200, login_good_message("登录成功", auth_token)
