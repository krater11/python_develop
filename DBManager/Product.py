import sqlite3
from DBManager.DBConnect import connectdb
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.DictZip import dict_zip_multiple, dict_zip


def upload_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_name = data["product_name"]
    product_introduction = data["product_introduction"]
    product_class_superset = data["product_class_superset"]

    c.execute(f"CREATE TABLE IF NOT EXISTS {product_class_superset} (product_id INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR,product_introduction VARCHAR,product_class_superset VARCHAR, type VARCHAR)")
    conn.commit()
    c.execute(f"INSERT INTO {product_class_superset} (name, product_introduction, product_class_superset, type) VALUES ('{product_name}', '{product_introduction}', '{product_class_superset}', 'product')")
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


def update_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_id = data["product_id"]
    superset = data["superset"]
    new_superset = data["new_superset"]
    key = []
    value = []
    if new_superset == "None":
        for k, v in data.items():
            if k == "product_id":
                continue
            elif k == "superset":
                continue
            elif k == "new_superset":
                continue
            key.append(k)
            value.append(v)
        update_query = f"UPDATE {superset} SET "
        count = 0
        for i in range(len(key) - 1):
            update_query += f"{key[count]} = '{value[count]}', "
            count += 1
        update_query += f"{key[count]} = '{value[count]}' WHERE product_id ={product_id}"
        c.execute(update_query)
        conn.commit()
        conn.close()
        return 200, normal_good_message("修改成功")

    table_item = c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{new_superset}'").fetchone()
    if table_item is None:
        return 400, bad_message("上一层级不存在")
    data_item = c.execute(f"SELECT * FROM {superset} WHERE product_id={product_id}").fetchall()[0]
    column_names = [description[0] for description in c.description]
    zip = dict_zip(data_item, column_names)
    for k, v in data.items():
        if k == "product_id":
            continue
        elif k == "superset":
            continue
        elif k == "new_superset":
            continue
        else:
            key.append(k)
            value.append(v)
    count = 0
    zip["product_class_superset"] = new_superset
    for i in value:
        zip[key[count]] = value[count]
        count += 1
    print(superset,new_superset)
    c.execute(f"DELETE FROM {superset} WHERE product_id ={product_id}")
    c.execute(f"INSERT INTO {new_superset} (name, product_introduction, product_class_superset, type) VALUES('{zip['name']}','{zip['product_introduction']}','{zip['product_class_superset']}', 'product')")
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_product(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    product_id = data["product_id"]
    superset = data["superset"]

    c.execute(f"DELETE FROM {superset} WHERE product_id = {product_id}")
    conn.commit()
    conn.close()

    return 200, normal_good_message("删除成功")