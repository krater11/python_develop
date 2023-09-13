import sqlite3
import uuid

from DBManager.DBConnect import connectdb
from DBManager.FindSubset import find_subset
from DBManager.GetSubset import get_subset
from utils.DictZip import dict_zip_multiple
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message, listdata_good_message


def get_subset_class(id):

    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")
    id_item = c.execute(f"SELECT id FROM ProductClass WHERE pid={id}").fetchall()
    id_list = []
    for i in id_item:
        id_list.append(i[0])
    return id_list


def get_subset(pid):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    item = c.execute(f"SELECT id, name, uuid, pid FROM ProductClass WHERE pid={pid}").fetchall()
    column_names = [description[0] for description in c.description]
    class_dict = dict_zip_multiple(item, column_names)
    for i in class_dict:
        if "children" not in i:
            i["children"] = get_subset(i["id"])
        else:
            i["children"] = i["children"].append(get_subset(i["id"]))
        i.pop("id")
    return class_dict


def upload_product_top_class(data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS ProductClass (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        pid INTEGER,
        uuid VARCHAR,
        rank VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    name = data["name"]
    pid = 0
    rank = "/"
    uuid_str = str(uuid.uuid4())
    class_data = (name, pid, uuid_str, rank)
    c.execute("INSERT INTO ProductClass (name, pid, uuid, rank) VALUES (?, ?, ?, ?)", class_data)

    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")


def upload_product_middle_class(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    name = data["name"]
    parent_uuid = data["uuid"]
    uuid_str = str(uuid.uuid4())

    pid = c.execute(f"SELECT id FROM ProductClass WHERE uuid='{parent_uuid}'").fetchone()[0]
    p_rank = c.execute(f"SELECT rank FROM ProductClass WHERE id={pid}").fetchone()[0]

    rank = p_rank + str(pid) + "/"
    class_data = (name, pid, uuid_str, str(rank))
    c.execute("INSERT INTO ProductClass (name, pid, uuid, rank) VALUES (?, ?, ?, ?)", class_data)
    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")


def get_product_class(pid=0):

    item = get_subset(pid)

    return 200, data_good_message("获取成功", "class_information", item)


def update_product_class(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    class_uuid = data["uuid"]
    name = data["name"]
    new_pid = data["pid"]
    class_id = c.execute(f"SELECT id FROM ProductClass WHERE uuid='{class_uuid}'").fetchone()[0]
    old_pid = c.execute(f"SELECT pid FROM ProductClass WHERE id={class_id}").fetchone()[0]

    if new_pid == old_pid:
        c.execute(f"UPDATE ProductClass SET name='{name}' WHERE id={class_id}")
        conn.commit()
        conn.close()
        return 200, normal_good_message("修改成功")

    pid_item = c.execute("SELECT pid FROM ProductClass").fetchall()
    pid_list = []
    for i in pid_item:
        if i[0] not in pid_list:
            pid_list.append(i[0])
    tree_list = []
    update_list = [class_id]
    get_list = update_list
    tree_list.append(update_list)
    count = 0
    while count < len(tree_list[-1]):
        tem_list = []
        for i in get_list:
            s_list = get_subset_class(i)
            if s_list not in tree_list and len(s_list) != 0:
                tree_list.append(s_list)
            for j in s_list:
                update_list.append(j)
                tem_list.append(j)
        get_list = tem_list
        for i in tree_list[-1]:
            if i not in pid_list:
                count += 1
            else:
                count = 0

    parent_rank = c.execute(f"SELECT rank FROM ProductClass WHERE id={new_pid}").fetchone()[0]
    new_rank = parent_rank + str(new_pid) + "/"
    c.execute(f"UPDATE ProductClass SET pid={new_pid},rank='{new_rank}' WHERE id={class_id}")
    for i in update_list[1:]:
        i_pid = c.execute(f"SELECT pid FROM ProductClass WHERE id={i}").fetchone()[0]
        p_rank = c.execute(f"SELECT rank FROM ProductClass WHERE id={i_pid}").fetchone()[0]
        rank = p_rank + str(i_pid) + "/"
        c.execute(f"UPDATE ProductClass SET rank='{rank}' WHERE id={i}")
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_product_class(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    pid_item = c.execute("SELECT pid FROM ProductClass").fetchall()
    pid_list = []
    for i in pid_item:
        if i[0] not in pid_list:
            pid_list.append(i[0])
    class_uuid = data["uuid"]
    class_id = c.execute(f"SELECT id FROM ProductClass WHERE uuid='{class_uuid}'").fetchone()[0]
    delete_list = [class_id]
    get_list = delete_list
    tree_list = []
    tree_list.append(delete_list)
    count = 0
    while count < len(tree_list[-1]):
        tem_list = []
        for i in get_list:
            s_list = get_subset_class(i)
            if s_list not in tree_list and len(s_list) != 0:
                tree_list.append(s_list)
            for j in s_list:
                delete_list.append(j)
                tem_list.append(j)
        get_list = tem_list
        for i in tree_list[-1]:
            if i not in pid_list:
                count += 1
            else:
                count = 0

    for i in delete_list:
        uuid = c.execute(f"SELECT uuid FROM ProductClass WHERE id={i}").fetchone()[0]
        c.execute(f"DELETE FROM ProductClass WHERE uuid='{uuid}'")
        c.execute(f"DELETE FROM Product WHERE class_uuid='{uuid}'")
    conn.commit()
    conn.close()

    return 200, normal_good_message("删除成功")