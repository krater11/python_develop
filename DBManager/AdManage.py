import json
import sqlite3
from datetime import datetime

from DBManager.DBConnect import connectdb
from utils.DictZip import dict_zip_multiple, dict_zip
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message, listdata_good_message


def upload_ad_text(data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS AdManage (
        text_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR,
        content VARCHAR,
        type VARCHAR,
        image VARCHAR,
        introduction VARCHAR,
        create_time VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    richtext_type = data["type"]
    title = data["title"]
    content = data["content"]
    image = data["image"]
    introduction = data["introduction"]
    create_time = str(datetime.now()).split(".")[0]
    text_data = (title, content, richtext_type, image, introduction, create_time)
    c.execute("INSERT INTO AdManage (title, content, type, image, introduction, create_time) VALUES (?, ?, ?, ?, ?, ?)", text_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("上传成功")


def get_ad_number(rich_text_type):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    text = c.execute("SELECT title, image, introduction, create_time FROM AdManage WHERE type = '%s'" % rich_text_type).fetchall()
    column_names = [description[0] for description in c.description]
    data = dict_zip_multiple(text, column_names)
    data_name_list = ["text_number", "text"]
    data_list = [len(data), data]
    return 200, listdata_good_message("获取成功", data_name_list, data_list)


def get_ad_text(text_id):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    text_item = c.execute("SELECT * FROM AdManage WHERE text_id = '%d'" % int(text_id)).fetchone()
    column_names = [description[0] for description in c.description]
    data = dict_zip(text_item, column_names)

    return 200, data_good_message("获取成功", "text_information", data)


# def get_ad_text(type_class, page):
#     try:
#         conn, c = connectdb()
#     except Exception:
#         return 400, bad_message("数据库连接失败")
#     type_number = c.execute("SELECT COUNT(*) FROM AdManage WHERE type = '%s'" % type_class).fetchall()[0][0]
#     text_page = int(page)
#     max_page = type_number//10 + 1
#     last_page_number = type_number - (max_page-1)*10
#     if max_page > text_page:
#         data = (type_class, 10, (text_page-1)*10)
#     else:
#         data = (type_class, last_page_number, (text_page-1)*10)
#     text_item = c.execute("SELECT * FROM AdManage WHERE type=? ORDER BY text_id LIMIT ? OFFSET ?", data)
#     column_names = [description[0] for description in c.description]
#     data = dict_zip_multiple(text_item, column_names)
#     json_data = json.dumps(data)
#     return 200, data_good_message("获取成功", "rich_text_information", json_data)


def update_ad_text(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")
    print(data)
    text_id = data["text_id"]
    key = []
    value = []
    for k, v in data.items():
        if k != "text_id":
            key.append(k)
            value.append(v)
    update_query = "UPDATE AdManage SET "
    count = 0
    for i in range(len(key) - 1):
        update_query += f"{key[count]} = '{value[count]}', "
        count += 1
    update_query += f"{key[count]} = '{value[count]}' WHERE text_id ={text_id}"
    c.execute(update_query)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_ad_text(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    text_id = data["text_id"]
    c.execute("DELETE FROM AdManage WHERE text_id =%d" % text_id)
    conn.commit()
    conn.close()

    return 200, normal_good_message("富文本删除成功")