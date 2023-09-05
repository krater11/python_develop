import sqlite3
from DBManager.DBConnect import connectdb
from DBManager.FindSubset import find_subset
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message


def upload_product_top_class(data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS ProductTopClassInfo (
        product_class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR,
        product_class_superset VARCHAR,
        type VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_class_name = data["product_class_name"]
    product_class_superset = data["product_class_superset"]
    class_type = data["type"]
    data = (product_class_name, product_class_superset, class_type)
    c.execute(
        "INSERT INTO ProductTopClassInfo (name, product_class_superset, type) VALUES (?, ?, ?)",
        data)
    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")


def upload_product_middle_class(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_class_name = data["product_class_name"]
    product_class_superset = data["product_class_superset"]
    class_type = data["type"]

    c.execute(f"CREATE TABLE IF NOT EXISTS {product_class_superset} (product_class_id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR,product_class_superset VARCHAR,type VARCHAR)")
    conn.commit()
    c.execute(f"INSERT INTO {product_class_superset} (name, product_class_superset, type) VALUES ('{product_class_name}', '{product_class_superset}','{class_type}')")
    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")


def get_product_class(name):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    name_item = c.execute(f"SELECT name FROM {name}").fetchall()
    name_list = []
    for i in name_item:
        name_list.append(i[0])

    return 200, data_good_message("获取成功", "product_class_list", name_list)


def update_product_class(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    superset = data["superset"]
    old_name = data["old_name"]
    current_name = data["current_name"]
    if superset == "None":
        c.execute(f"UPDATE ProductTopClassInfo SET name = '{current_name}' WHERE name='{old_name}'")
        c.execute(f"ALTER TABLE '{old_name}' RENAME TO '{current_name}'")
        c.execute(f"UPDATE '{current_name}' SET product_class_superset = '{current_name}'")
        conn.commit()
        conn.close()
        return 200, normal_good_message("修改成功")
    c.execute(f"UPDATE {superset} SET name = '{current_name}' WHERE name='{old_name}'")
    c.execute(f"ALTER TABLE '{old_name}' RENAME TO '{current_name}'")
    c.execute(f"UPDATE '{current_name}' SET product_class_superset = '{current_name}'")
    conn.commit()
    conn.close()

    return 200, normal_good_message("修改成功")


def delete_product_class(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    superset = data["superset"]
    product_class_id = data["product_class_id"]

    if superset == "None":
        item = c.execute(f"SELECT name, type FROM ProductTopClassInfo WHERE product_class_id={product_class_id}").fetchone()
        delete_list = []
        delete_list.append(item[0])
        item = c.execute(f"SELECT name, type FROM {item[0]}").fetchall()
        c.execute(f"DELETE FROM ProductTopClassInfo WHERE product_class_id={product_class_id}")
        for i in item:
            delete_list.append(i[0])
        for i in delete_list:
            c.execute(f"DROP TABLE IF EXISTS {i}")
        conn.commit()
        conn.close()
        return 200, normal_good_message("删除成功")

    subset_item = c.execute(f"SELECT name FROM {superset} WHERE product_class_id={product_class_id}").fetchone()

    c.execute(f"DELETE FROM {superset} WHERE product_class_id = {product_class_id}")
    c.execute(f"DROP TABLE IF EXISTS {subset_item[0]}")
    conn.commit()
    conn.close()
    return 200, normal_good_message("删除成功")