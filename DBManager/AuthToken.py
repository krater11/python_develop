import sqlite3
from settings import DATABASE
from utils.HashNumber import hash_string


def BasicAuth(user_name,user_password):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, "连接失败"

    item = c.execute("SELECT user_password FROM UserInfo WHERE user_name = '%s'" % user_name)
    useritem = item.fetchone()

    if useritem is None:
        conn.close()
        return 400, "账号不存在，用户验证失败"

    userpassword = hash_string(user_password)
    if userpassword != useritem[0]:
        conn.close()
        return 400, "密码错误，用户验证失败"

    return 200, "用户验证成功"

