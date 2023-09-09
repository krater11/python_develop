import sqlite3
from DBManager.DBConnect import connectdb
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.DictZip import dict_zip_multiple, dict_zip


def upload_product(data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        product_class VARCHAR,
        name VARCHAR,
        product_introduction VARCHAR,
        image VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    class_id = data["class_id"]
    product_class = data["product_class"]
    name = data["name"]
    introduction = data["product_introduction"]
    image = data["image"]
    post_data = (class_id, product_class, name, introduction, image)
    c.execute("INSERT INTO Product (class_id, product_class, name, product_introduction, image) VALUES (?, ?, ?, ?, ?)", post_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("保存成功")


def get_product(product_class_id):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_item = c.execute(f"SELECT id, name FROM Product WHERE class_id={product_class_id}").fetchall()
    column_names = [description[0] for description in c.description]
    product_list = dict_zip_multiple(product_item, column_names)

    return 200, data_good_message("数据获取成功", "product_information", product_list)


def get_product_detail(product_id):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_item = c.execute(f"SELECT * FROM Product WHERE id={product_id}").fetchall()
    column_names = [description[0] for description in c.description]
    product_list = dict_zip_multiple(product_item, column_names)

    return 200, data_good_message("数据获取成功", "product_detail_information", product_list)


def update_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_id = data["product_id"]
    key = []
    value = []
    for k, v in data.items():
        if k != "product_id":
            key.append(k)
            value.append(v)
    update_query = "UPDATE Product SET "
    count = 0
    for i in range(len(key) - 1):
        update_query += f"{key[count]} = '{value[count]}', "
        count += 1
    update_query += f"{key[count]} = '{value[count]}' WHERE id ={product_id}"
    c.execute(update_query)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_id = data["product_id"]

    c.execute(f"DELETE FROM Product WHERE product_id = {product_id}")
    conn.commit()
    conn.close()

    return 200, normal_good_message("删除成功")
