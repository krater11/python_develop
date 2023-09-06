import sqlite3

from DBManager.DBConnect import connectdb
from utils.ResponseBadMessage import bad_message


def get_subset(name):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    item = c.execute(f"SELECT type FROM {name} limit 1").fetchone()

    if item[0] == "product":
        return True, []
    else:
        subset_item = c.execute(f"SELECT name FROM {name}").fetchall()
        name_list = []
        for i in subset_item:
            name_list.append(i[0])

        return False, name_list
