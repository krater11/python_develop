import json
import sqlite3

from DBManager.DBConnect import connectdb
from settings import DATABASE
from utils.GetID import get_id
from utils.DictZip import dict_zip_multiple
from utils.PermissionSwift import permission_swift, permission_number
from DBManager.UserInfo import GetUserId
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message


# 获取该用户名是否是管理者用户
def get_superuser_status(username):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("连接失败")

    superuseritem = c.execute("SELECT superuser FROM UserInfo WHERE user_name = '%s'" % username).fetchone()
    conn.close()
    return superuseritem[0]


# 获取除管理者用户外的全部用户权限
def get_user_permission():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("连接失败")

    superuseritem = c.execute("SELECT user_id FROM UserInfo WHERE superuser = 1").fetchall()
    data = tuple(get_id(superuseritem))
    select_query = f"SELECT * FROM PermissionInfo WHERE 1=1"
    for i in data:
        select_query += f" AND user_id != {i}"
    useritem = c.execute(select_query).fetchall()
    permission_list = permission_swift(useritem)
    column_names = [description[0] for description in c.description]
    column_names[0] = "user_name"
    dictzip = dict_zip_multiple(permission_list, column_names)
    json_data = json.dumps(dictzip)
    conn.close()
    return 200, data_good_message("获取成功", "用户权限信息", json_data)


def manage_permission(data):

    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    username = data['user_name']
    userid = GetUserId(username)
    upload_permission = data["upload_permission"]
    read_permission = data["read_permission"]
    update_permission = data["update_permission"]
    list = [upload_permission, read_permission, update_permission]
    permission_list = permission_number(list)
    permission_list += [userid]
    try:
        c.execute("UPDATE PermissionInfo SET upload_permission = ?, read_permission = ?, update_permission = ? WHERE user_id = ?", permission_list)
        conn.commit()
    except Exception:
        return 400, bad_message("连接失败")
    conn.close()
    return 200, normal_good_message("权限更改成功")