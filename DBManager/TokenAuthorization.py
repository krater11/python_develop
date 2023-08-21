import sqlite3
from settings import DATABASE


def token_authorization(token):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return "", 400

    tokenitem = c.execute("SELECT user_name FROM UserInfo WHERE user_token = '%s'" % token).fetchone()[0]
    if tokenitem is None:
        return "", 400

    return tokenitem, 200
