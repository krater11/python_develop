import sqlite3

from DBManager.DBConnect import connectdb
from utils.DictZip import dict_zip
from settings import DATABASE
from utils.ResponseBadMessage import bad_message


def permission_status(username):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    item = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()
    userid = useritem[0]
    item1 = c.execute("SELECT * FROM PermissionInfo WHERE user_id = '%d'" % userid)
    permissionitem = item1.fetchone()
    column_names = [description[0] for description in c.description][-3:]
    permissionstatus = permissionitem[-3:]
    data = dict_zip(permissionstatus, column_names)

    return data
