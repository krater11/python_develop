import sqlite3
from utils.DictZip import dict_zip


def permission_status(username):
    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "连接失败"

    item = c.execute("SELECT user_id FROM UserInfo WHERE user_name = '%s'" % username)
    useritem = item.fetchone()
    userid = useritem[0]
    item1 = c.execute("SELECT * FROM PermissionInfo WHERE user_id = '%d'" % userid)
    permissionitem = item1.fetchone()
    column_names = [description[0] for description in c.description][-3:]
    permissionstatus = permissionitem[-3:]
    data = dict_zip(permissionstatus, column_names)

    return data
