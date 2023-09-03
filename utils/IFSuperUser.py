import sqlite3
from settings import DATABASE


def if_superuser(username):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        print("连接失败")

    superuser_status = c.execute("SELECT superuser FROM UserInfo WHERE user_name = '%s'" % username).fetchone()[0]

    if superuser_status == 0:
        return False
    else:
        return True