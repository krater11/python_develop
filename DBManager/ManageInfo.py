import sqlite3
from utils.HashNumber import hash_string
from settings import DATABASE
from datetime import datetime


def ManageRegist(username, userpassword, userphone):
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
        return 401, "链接失败"

    item = c.execute("SELECT user_name FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()

    if useritem is not None:
        conn.close()
        return 400, "用户名已存在"

    hashuserpassword = hash_string(userpassword)
    createtime = datetime.now()
    usercreatetime = createtime.strftime("%Y-%m-%d %H:%M:%S")
    data = (username, hashuserpassword, userphone, usercreatetime, 1)
    c.execute("INSERT INTO UserInfo (user_name, user_password, user_phone, user_createtime, superuser) VALUES(?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return 200, "注册成功"


def ManageLogin(username, userpassword,auth_token):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 401, "链接失败"

    hashpassword = hash_string(userpassword)

    useritem = c.execute("SELECT user_password FROM UserInfo WHERE user_name = '%s'" % username).fetchone()
    if useritem is None:
        conn.close()
        return 400, "用户不存在"
    if not hashpassword == useritem[0]:
        conn.close()
        return 400, "密码错误"

    conn.execute('''
    CREATE TABLE IF NOT EXISTS PermissionInfo (
    user_id INTEGER REFERENCES UserInfo (user_id),
    upload_permission VARCHAR,
    read_permission VARCHAR,
    update_permission VARCHAR)''')
    user_id = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]
    if c.execute("SELECT user_id FROM PermissionInfo WHERE user_id = '%d'" % user_id).fetchone() is None:
        c.execute("INSERT INTO PermissionInfo (user_id, upload_permission, read_permission, update_permission) VALUES(? ,?, ?, ?)", (user_id, 1, 1, 1))
        conn.commit()

    user_item = c.execute("SELECT user_token FROM UserInfo WHERE user_name = '%s'" % username).fetchone()
    if user_item[0] is not None:
        conn.close()
        return 200, "登录成功"
    c.execute("UPDATE UserInfo SET user_token = ? WHERE user_name = ?", (auth_token, username))

    conn.commit()
    conn.close()
    return 200, "登录成功"