import sqlite3
from DBManager.DBConnect import connectdb
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message


def upload_product_top_class(data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS ProductTopClassInfo (
        product_class_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_class_name VARCHAR,
        product_class_superset VARCHAR,
        product_class_subset VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_class_name = data["product_class_name"]
    product_class_superset = data["product_class_superset"]
    data = (product_class_name, product_class_superset)
    c.execute(
        "INSERT INTO ProductTopClassInfo (product_class_name, product_class_superset) VALUES (?, ?)",
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

    c.execute(f"CREATE TABLE IF NOT EXISTS {product_class_superset} (product_class_id INTEGER PRIMARY KEY AUTOINCREMENT,product_class_name VARCHAR,product_class_superset VARCHAR,product_class_subset VARCHAR)")
    conn.commit()
    c.execute(f"INSERT INTO {product_class_superset} (product_class_name, product_class_superset) VALUES ('{product_class_name}', '{product_class_superset}')")
    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")