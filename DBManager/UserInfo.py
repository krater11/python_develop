import sqlite3
from datetime import datetime
from utils.hash import hash_string
from utils.TokenCreate import generate_token
from utils.DictZip import dict_zip
from settings import DATABASE


def UserRegist(username,userpassword,userphone):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 401, "链接失败"

    item = c.execute("SELECT user_name FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()

    if useritem is not None:
        c.close()
        conn.close()
        return 400, "用户名已存在"

    hashuserpassword = hash_string(userpassword)
    createtime = datetime.now()
    usercreatetime = createtime.strftime("%Y-%m-%d %H:%M:%S")
    data = (username, hashuserpassword, userphone, usercreatetime)
    c.execute("INSERT INTO UserInfo (user_name, user_password, user_phone, user_createtime) VALUES(?, ?, ?, ?)", data)
    conn.commit()
    c.close()
    conn.close()
    return 200, "注册成功"


def UserLogin(username,userpassword):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 401, "链接失败"

    hashpassword = hash_string(userpassword)
    item = c.execute("SELECT * FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()
    if useritem is None:
        c.close()
        conn.close()
        return 400, "用户不存在"

    item1 = c.execute("SELECT * FROM UserInfo WHERE user_name = '%s'" % username)
    useritem1 = item1.fetchall()

    column_names = [description[0] for description in c.description]

    data = dict_zip(useritem1, column_names)

    if not hashpassword == data["user_password"]:
        c.close()
        conn.close()
        return 400, "密码错误"
    user_token = generate_token()
    item = c.execute("SELECT user_token FROM UserInfo WHERE user_name = '%s'" % username)
    user_item = item.fetchone()
    if user_item[0] is not None:
        print("one")
        c.close()
        conn.close()
        return 200, "登录成功"
    c.execute("UPDATE UserInfo SET user_token = '%s'" % user_token)
    conn.commit()
    c.close()
    conn.close()
    return 200, "登录成功"