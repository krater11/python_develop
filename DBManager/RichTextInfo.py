import os
import sqlite3
import uuid
from pathlib import Path
from DBManager.DBConnect import connectdb
from settings import DATABASE, ROOT_PATH, FILE_PATH
from utils.DictZip import dict_zip, dict_zip_multiple
import json
import socket
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message

root_path = ROOT_PATH.replace("\\", "/")
image_path = FILE_PATH + "/" + "rich_text_image/"
real_path = root_path + image_path


def upload_rich_text(data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS RichTextInfo (
        text_id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_name VARCHAR,
        text VARCHAR,
        type VARCHAR
        )
        ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    richtext_type = data["type"]
    text_name = data["text_name"]
    text = data["text"]
    text_data = (text_name, text, richtext_type)
    Path(real_path.replace("/", "\\")).mkdir(parents=True, exist_ok=True)
    c.execute(
        "INSERT INTO RichTextInfo (text_name, text, type) VALUES (?, ?, ?)",
        text_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("保存成功")


def get_rich_text(rich_text_type):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    textitem = c.execute("SELECT * FROM RichTextInfo WHERE type = '%s'" % rich_text_type).fetchall()
    column_names = [description[0] for description in c.description]
    data = dict_zip_multiple(textitem, column_names)
    json_data = json.dumps(data)
    return 200, data_good_message("获取成功", "rich_text_information", json_data)


def update_rich_text(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")
    text_id = data["text_id"]
    key = []
    value = []
    for k, v in data.items():
        if k != "text_id":
            key.append(k)
            value.append(v)
    update_query = "UPDATE RichTextInfo SET "
    count = 0
    for i in range(len(key) - 1):
        update_query += f"{key[count]} = '{value[count]}', "
        count += 1
    update_query += f"{key[count]} = '{value[count]}' WHERE text_id ={text_id}"
    c.execute(update_query)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_rich_text(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    text_id = data["text_id"]
    c.execute("DELETE FROM RichTextInfo WHERE text_id =%d" % text_id)
    conn.commit()
    conn.close()

    return 200, normal_good_message("富文本删除成功")

