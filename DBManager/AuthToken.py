import sqlite3

from DBManager.DBConnect import connectdb
from settings import DATABASE
from utils.HashNumber import hash_string
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message


def BasicAuth(user_name,user_password):

    try:
        conn, c = connectdb()
    except Exception:
        return 400

    item = c.execute("SELECT user_password FROM UserInfo WHERE user_name = '%s'" % user_name)
    useritem = item.fetchone()

    if useritem is None:
        conn.close()
        return 400

    userpassword = hash_string(user_password)
    if userpassword != useritem[0]:
        conn.close()
        return 400

    return 200

