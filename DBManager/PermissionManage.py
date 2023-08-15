import sqlite3
from utils.DictZip import dict_zip_multiple
from utils.PermissionSwift import permission_swift
import json


def get_superuser_status(username):

    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "连接失败"

    superuseritem = c.execute("SELECT superuser FROM UserInfo WHERE user_name = '%s'" % username).fetchone()

    return superuseritem[0]


def get_user_permission(username):

    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "连接失败"
    superuseritem = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username).fetchone()
    userid = superuseritem[0]
    useritem = c.execute("SELECT * FROM PermissionInfo WHERE user_id != '%d'" % userid).fetchall()
    permission_list = permission_swift(useritem)
    column_names = [description[0] for description in c.description]
    dictzip = dict_zip_multiple(permission_list, column_names)
    json_data = json.dumps(dictzip)
    return 200, json_data