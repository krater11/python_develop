import sqlite3
from settings import DATABASE
from utils.DictZip import dict_zip
import json
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message


def upload_rich_text(data):
    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS RichTextInfo (
        text_id INTEGER PRIMARY KEY AUTOINCREMENT,
        text_name VARCHAR,
        text VARCHAR,
        text_font VARCHAR,
        text_color VARCHAR,
        text_bold VARCHAR,
        text_italic VARCHAR
        )
        ''')
        c = conn.cursor()
    except Exception:
        return 400, bad_message("连接失败")
    text_name = data["text_name"]
    text = data["text"]
    text_font = data["text_font"]
    text_color = data["text_color"]
    text_bold = data["text_bold"]
    text_italic = data["text_italic"]
    text_data = tuple([text_name, text, text_font, text_color, text_bold, text_italic])
    textitem = c.execute("SELECT text_id FROM RichTextInfo WHERE text_name = '%s'" % text_name).fetchone()
    if textitem is not None:
        return 400, bad_message("连接失败")

    try:
        c.execute(
            "INSERT INTO RichTextInfo (text_name, text, text_font, text_color, text_bold, text_italic) VALUES (?, ?, ?, ?, ?, ?)",
            text_data)
        conn.commit()
        conn.close()
    except Exception:
        print(Exception)
    return 200, normal_good_message("保存成功")


def get_rich_text(textname):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("连接失败")

    textitem = c.execute("SELECT * FROM RichTextInfo WHERE text_name = '%s'" % textname).fetchall()
    column_names = [description[0] for description in c.description]
    data = dict_zip(textitem[0], column_names)
    json_data = json.dumps(data)
    return 200, data_good_message("获取成功", "富文本信息", json_data)


def update_rich_text(data):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("连接失败")

    richtextitem = c.execute("SELECT * FROM RichTextInfo WHERE text_name = '%s'" % data["text_name"]).fetchone()
    if richtextitem is None:
        conn.close()
        return 400, bad_message("文本不存在")

    key = []
    value = []
    for k, v in data.items():
        if k == "text_name":
            text_name = v
        else:
            key.append(k)
            value.append(v)
    update_query = "UPDATE RichTextInfo SET "
    count = 0
    for i in range(len(key) - 1):
        update_query += f'{key[count]} = {value[count]}, '
        count += 1
    update_query += f"{key[count]} = {value[count]} WHERE text_name = '{text_name}'"
    c.execute(update_query)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_rich_text(data):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("数据库连接失败")

    richtextitem = c.execute("SELECT * FROM RichTextInfo WHERE text_name = '%s'" % data["text_name"]).fetchone()
    if richtextitem is None:
        conn.close()
        return 400, bad_message("文本不存在")

    c.execute("DELETE FROM RichTextInfo WHERE text_name = '%s'" % data["text_name"])
    conn.commit()
    conn.close()

    return 200, normal_good_message("富文本删除成功")
