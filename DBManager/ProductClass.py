import sqlite3
from DBManager.DBConnect import connectdb
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