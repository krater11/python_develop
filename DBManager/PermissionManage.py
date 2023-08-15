import json
import sqlite3
from utils.GetID import get_id
from utils.DictZip import dict_zip_multiple
from utils.PermissionSwift import permission_swift


# 获取该用户名是否是管理者用户
def get_superuser_status(username):
    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "连接失败"

    superuseritem = c.execute("SELECT superuser FROM UserInfo WHERE user_name = '%s'" % username).fetchone()

    return superuseritem[0]


# 获取除管理者用户外的全部用户权限
def get_user_permission():
    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "连接失败"

    superuseritem = c.execute("SELECT user_id FROM UserInfo WHERE superuser = 1").fetchall()
    data = tuple(get_id(superuseritem))
    select_query = f"SELECT * FROM PermissionInfo WHERE 1=1"
    for i in data:
        select_query += f" AND user_id != {i}"
    useritem = c.execute(select_query).fetchall()
    permission_list = permission_swift(useritem)
    column_names = [description[0] for description in c.description]
    dictzip = dict_zip_multiple(permission_list, column_names)
    json_data = json.dumps(dictzip)
    return 200, json_data
