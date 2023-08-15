import sqlite3
from settings import DATABASE


def id_swift_name(id):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        print("error")

    username = c.execute("SELECT user_name FROM UserInfo WHERE user_id = '%d' " % id).fetchone()[0]

    return username


def permission_swift(a):
    permissionlist = []
    for i in a:
        row_list = []
        for x in i:
            if x == "1":
                row_list.append("True")
            elif x == "0":
                row_list.append("False")
            else:
                name = id_swift_name(x)
                row_list.append(name)
            row_tuple = tuple(row_list)
        permissionlist.append(row_tuple)

    return permissionlist


def permission_number(data):
    permission_list = []
    for i in data:
        if i == "True":
            permission_list.append("1")
        else:
            permission_list.append("0")
    return permission_list
