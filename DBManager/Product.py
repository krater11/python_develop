import sqlite3
import uuid

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
        class_uuid VARCHAR,
        product_class VARCHAR,
        name VARCHAR,
        product_introduction VARCHAR,
        image VARCHAR,
        uuid VARCHAR,
        text VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    print(data)
    class_uuid = data["class_uuid"]
    product_class = data["product_class"]
    name = data["name"]
    introduction = data["product_introduction"]
    text = data["text"]
    image = data["image"]
    uuid_str = str(uuid.uuid4())

    post_data = (class_uuid, product_class, name, introduction, image, uuid_str, text)
    c.execute("INSERT INTO Product (class_uuid, product_class, name, product_introduction, image, uuid, text) VALUES (?, ?, ?, ?, ?, ?, ?)", post_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("保存成功")


def get_product():
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_item = c.execute(f"SELECT uuid, name, product_class FROM Product").fetchall()
    column_names = [description[0] for description in c.description]
    product_list = dict_zip_multiple(product_item, column_names)

    return 200, data_good_message("数据获取成功", "product_information", product_list)


def get_product_detail(product_uuid):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_item = c.execute(f"SELECT * FROM Product WHERE uuid='{product_uuid}'").fetchall()
    column_names = [description[0] for description in c.description]
    product_list = dict_zip_multiple(product_item, column_names)
    return 200, data_good_message("数据获取成功", "product_detail_information", product_list[0])


def update_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    print(data)
    product_uuid = data["uuid"]
    key = []
    value = []
    for k, v in data.items():
        if k == "id":
            continue
        if k == "uuid":
            continue
        key.append(k)
        value.append(v)
    update_query = "UPDATE Product SET "
    count = 0
    for i in range(len(key) - 1):
        update_query += f"{key[count]} = '{value[count]}', "
        count += 1
    update_query += f"{key[count]} = '{value[count]}' WHERE uuid ='{product_uuid}'"
    c.execute(update_query)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_uuid = data["product_uuid"]

    c.execute(f"DELETE FROM Product WHERE uuid = '{product_uuid}'")
    conn.commit()
    conn.close()

    return 200, normal_good_message("删除成功")
