import sqlite3
from settings import DATABASE
from utils.IfTime import if_expire_time


def token_authorization(token):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return "", 400

    tokenitem = c.execute("SELECT token_expire_time FROM UserInfo WHERE user_token = '%s'" % token).fetchone()[0]
    if tokenitem is None:
        return "", 400

    if if_expire_time(tokenitem):
        return "", 400
    username = c.execute("SELECT user_name FROM UserInfo WHERE user_token = '%s'" % token).fetchone()[0]
    return username, 200