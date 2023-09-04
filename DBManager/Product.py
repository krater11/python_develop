import sqlite3
from DBManager.DBConnect import connectdb
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.DictZip import dict_zip_multiple


def upload_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_name = data["product_name"]
    product_introduction = data["product_introduction"]
    product_class = data["product_class"]

    c.execute(f"CREATE TABLE IF NOT EXISTS {product_class} (product_id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR,product_introduction VARCHAR,product_class VARCHAR)")
    conn.commit()
    c.execute(f"INSERT INTO {product_class} (name, product_introduction, product_class) VALUES ('{product_name}', '{product_introduction}', '{product_class}')")
    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")


def get_product(product_class):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    name_item = c.execute(f"SELECT * FROM {product_class}").fetchall()
    column_names = [description[0] for description in c.description]
    name_list = dict_zip_multiple(name_item, column_names)

    return 200, data_good_message("数据获取成功", "product_information", name_list)