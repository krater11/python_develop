import json
import sqlite3
from datetime import datetime
from utils.HashNumber import hash_string
from settings import DATABASE, RESPONSE_BAD_MESSAGE, RESPONSE_GOOD_MESSAGE
from utils.IFSuperUser import if_superuser
from utils.GenerateToken import generate_token
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import login_good_message, normal_good_message


def UserRegist(user_data):
    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS UserInfo (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR UNIQUE,
    user_password VARCHAR,
    user_phone INTEGER (11),
    user_createtime DATETIME,
    user_token VARCHAR (255),
    superuser INTEGER)''')
        c = conn.cursor()
    except Exception:
        return 400, bad_message("链接失败")

    username = user_data["user_name"]
    userpassword = user_data["user_password"]
    userphone = user_data["user_phone"]
    item = c.execute("SELECT user_name FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()

    if useritem is not None:
        conn.close()
        return 400, bad_message("链接失败")

    hashuserpassword = hash_string(userpassword)
    createtime = datetime.now()
    usercreatetime = createtime.strftime("%Y-%m-%d %H:%M:%S")
    data = (username, hashuserpassword, userphone, usercreatetime, 0)
    c.execute("INSERT INTO UserInfo (user_name, user_password, user_phone, user_createtime, superuser) VALUES(?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("注册成功")


def UserLogin(data):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("链接失败")

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
    CREATE TABLE IF NOT EXISTS PermissionInfo (user_id INTEGER REFERENCES UserInfo (user_id),
    upload_permission VARCHAR,
    read_permission VARCHAR,
    update_permission VARCHAR)''')

    if if_superuser(username):
        print("管理员用户")
        user_id = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]
        if c.execute("SELECT user_id FROM PermissionInfo WHERE user_id = '%d'" % user_id).fetchone() is None:
            c.execute(
                "INSERT INTO PermissionInfo (user_id, upload_permission, read_permission, update_permission) VALUES(? ,?, ?, ?)",
                (user_id, 1, 1, 1))
            conn.commit()
    else:
        print("普通用户")
        user_id = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]
        if c.execute("SELECT user_id FROM PermissionInfo WHERE user_id = '%d'" % user_id).fetchone() is None:
            c.execute(
                "INSERT INTO PermissionInfo (user_id, upload_permission, read_permission, update_permission) VALUES(? ,?, ?, ?)",
                (user_id, 0, 1, 0))
            conn.commit()

    auth_token = generate_token(username, userpassword)
    user_item = c.execute("SELECT user_token FROM UserInfo WHERE user_name = '%s'" % username).fetchone()
    if user_item[0] is not None:
        conn.close()
        return 200, login_good_message("登录成功", user_item[0])
    c.execute("UPDATE UserInfo SET user_token = ? WHERE user_name = ?", (auth_token, username))

    conn.commit()
    conn.close()
    return 200, login_good_message("登录成功", auth_token)


def GetUserId(username):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        print("error")

    userid = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]

    return userid
