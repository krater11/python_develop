import os
import sqlite3
import uuid
from pathlib import Path
from DBManager.DBConnect import connectdb
from settings import DATABASE, ROOT_PATH, IMAGE_PATH
from utils.DictZip import dict_zip, dict_zip_multiple
import json
import socket
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.ResponseBadMessage import bad_message

root_path = ROOT_PATH.replace("\\", "/")
image_path = IMAGE_PATH + "/" + "rich_text_image/"
real_path = root_path + image_path


def upload_rich_text(imagename, imagefile, data):
    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS RichTextInfo (
        text_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR,
        text_name VARCHAR,
        text VARCHAR,
        text_font VARCHAR,
        text_color VARCHAR,
        text_bold VARCHAR,
        text_italic VARCHAR,
        type VARCHAR
        )
        ''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS RichTextImage (
        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name VARCHAR,
        image_path VARCHAR,
        text_name VARCHAR REFERENCES RichTextInfo (text_name))''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    richtext_type = data["type"]
    text_name = data["text_name"]
    text = data["text"]
    text_font = data["text_font"]
    text_color = data["text_color"]
    text_bold = data["text_bold"]
    text_italic = data["text_italic"]
    text_data = (text_name, text, text_font, text_color, text_bold, text_italic, richtext_type)
    Path(real_path.replace("/", "\\")).mkdir(parents=True, exist_ok=True)
    richtextitem = c.execute("SELECT text_id FROM RichTextInfo WHERE text_name='%s'" % text_name).fetchone()
    if richtextitem is not None:
        conn.close()
        return 400, bad_message("名称已存在")
    c.execute(
        "INSERT INTO RichTextInfo (text_name, text, text_font, text_color, text_bold, text_italic,  type) VALUES (?, ?, ?, ?, ?, ?, ?)",
        text_data)
    count = 0
    for i in imagename:
        file_type = i.split(".")[-1]
        generate_uuid = uuid.uuid4()
        name_list = [str(generate_uuid), file_type]
        image_name = ".".join(name_list)
        with open(real_path + image_name, 'wb') as f:
            f.write(imagefile[count])
        count += 1
        image_data = (image_name, image_path, text_name)
        c.execute("INSERT INTO RichTextImage (image_name, image_path, text_name) VALUES (?, ?, ?)", image_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("保存成功")


def get_rich_text(rich_text_type):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    textitem = c.execute("SELECT * FROM RichTextInfo WHERE type = '%s'" % rich_text_type).fetchall()
    print(textitem)
    column_names = [description[0] for description in c.description]
    data = dict_zip_multiple(textitem, column_names)
    ip = socket.gethostbyname(socket.gethostname())
    for i in data:
        text_name = i["text_name"]
        image_item = c.execute("SELECT * FROM RichTextImage WHERE text_name = '%s'" % text_name).fetchall()
        column_names = [description[0] for description in c.description]
        image_data = dict_zip_multiple(image_item, column_names)
        image = []
        for j in image_data:
            str = "http://" + ip + ":8000" + j["image_path"] + j["image_name"]
            image.append(str)
        i["image"] = image
    json_data = json.dumps(data)
    return 200, data_good_message("获取成功", "富文本信息", json_data)


def update_rich_text(imagename, imagefile, data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")
    text_id = data["text_id"]
    origin_text_name = c.execute(f"SELECT text_name FROM RichTextInfo WHERE text_id ={text_id}").fetchone()[0]
    text_id = data["text_id"]
    if imagename[0] == None:
        key = []
        value = []
        for k, v in data.items():
            key.append(k)
            value.append(v)
        update_query = "UPDATE RichTextInfo SET "
        count = 0
        for i in range(len(key) - 1):
            update_query += f"{key[count]} = '{value[count]}', "
            count += 1
        update_query += f"{key[count]} = '{value[count]}' WHERE text_id ={text_id}"
        current_text_name = data["text_name"]
        c.execute(f"UPDATE RichTextImage SET text_name={current_text_name} WHERE text_name={origin_text_name}")
        c.execute(update_query)
    else:
        key = []
        value = []
        for k, v in data.items():
            key.append(k)
            value.append(v)
        update_query = "UPDATE RichTextInfo SET "
        count = 0
        for i in range(len(key) - 1):
            update_query += f"{key[count]} = '{value[count]}', "
            count += 1
        update_query += f"{key[count]} = '{value[count]}' WHERE text_id ={text_id}"
        current_text_name = data["text_name"]
        c.execute(f"UPDATE RichTextImage SET text_name={current_text_name} WHERE text_name={origin_text_name}")
        c.execute(update_query)
        count1 = 0
        for i in imagename:
            file_type = i.split(".")[-1]
            generate_uuid = uuid.uuid4()
            name_list = [str(generate_uuid), file_type]
            image_name = ".".join(name_list)
            with open(real_path + image_name, 'wb') as f:
                f.write(imagefile[count1])
            count1 += 1
            image_data = (image_name, image_path, current_text_name)
            c.execute("INSERT INTO RichTextImage (image_name, image_path, text_name) VALUES (?, ?, ?)", image_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_rich_text(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    text_id = data["text_id"]
    text_name = c.execute(f"SELECT text_name FROM RichTextInfo WHERE text_id={text_id}").fetchone()[0]
    image_item = c.execute("SELECT * FROM RichTextImage WHERE text_name='%s'" % text_name).fetchall()
    column_names = [description[0] for description in c.description]
    dict_data = dict_zip_multiple(image_item,column_names)
    for i in dict_data:
        image_path = root_path+i["image_path"]+i["image_name"]
        os.remove(image_path)
    c.execute("DELETE FROM RichTextImage WHERE text_name ='%s'" % text_name)
    c.execute("DELETE FROM RichTextInfo WHERE text_id =%d" % text_id)
    conn.commit()
    conn.close()

    return 200, normal_good_message("富文本删除成功")


def delete_rich_text_image(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    url = data["url"]
    url_list = url.split(",")
    for i in url_list:
        detail_list = url.split("/")
        if detail_list[-2] != "rich_text_image":
            return 400, bad_message("url错误")
        image_name = detail_list[-1]
        image_path = c.execute("SELECT image_path FROM RichTextImage WHERE image_name='%s'" % image_name).fetchone()[0]
        detail_path = root_path + image_path + image_name
        os.remove(detail_path)
        c.execute("DELETE FROM RichTextImage WHERE image_name ='%s'" % image_name)
    conn.commit()
    conn.close()
    return 200, normal_good_message("富文本图片删除成功")