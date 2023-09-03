import sqlite3
from DBManager.DBConnect import connectdb
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message


def upload_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_name = data["product_name"]
    product_introduction = data["product_introduction"]
    product_class = data["product_class"]

    c.execute(f"CREATE TABLE IF NOT EXISTS {product_class} (product_id INTEGER PRIMARY KEY AUTOINCREMENT,product_name VARCHAR,product_introduction VARCHAR,product_class VARCHAR)")
    conn.commit()
    c.execute(f"INSERT INTO {product_class} (product_name, product_introduction, product_class) VALUES ('{product_name}', '{product_introduction}', '{product_class}')")
    conn.commit()
    conn.close()

    return 200, normal_good_message("保存成功")