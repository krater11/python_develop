import json
import os
import uuid
from pathlib import Path
import socket
from DBManager.DBConnect import connectdb
from settings import ROOT_PATH, FILE_PATH
from utils.GuessType import guess_type
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import data_good_message, normal_good_message
from utils.DictZip import dict_zip_multiple
from utils.UpdateList import update_list, tuple_list


def upload_ad(imagename, imagefile, data):

    try:
        conn, c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Ad_image (
        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name VARCHAR,
        image_path VARCHAR)''')
        conn.execute('''
        CREATE TABLE IF NOT EXISTS Ad_information (
        text_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR,
        content VARCHAR,
        image_name VARCHAR REFERENCES Ad_image (image_name),
        type VARCHAR)''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    type = data["type"]
    title = data["title"]
    content = data["content"]
    root_path = ROOT_PATH.replace("\\", "/")
    file_type = imagename.split(".")[-1]
    generate_uuid = uuid.uuid4()
    name_list = [str(generate_uuid), file_type]
    imagefile_name = ".".join(name_list)
    file_path = guess_type(file_type) + "/ad_image/"
    real_path = root_path + file_path
    Path(real_path.replace("/", "\\")).mkdir(parents=True, exist_ok=True)
    image_data = (imagefile_name, file_path)
    information_data = (title, content, imagefile_name, type)
    with open(root_path+file_path+imagefile_name, 'wb') as f:
        f.write(imagefile)
    c.execute("INSERT INTO Ad_image (image_name, image_path) VALUES (?, ?)", image_data)
    c.execute("INSERT INTO Ad_information (title, content, image_name, type) VALUES (?, ?, ?, ?)", information_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("上传成功")


def get_ad_information(data):
    try:
        conn,c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")
    aditem = c.execute("SELECT * FROM Ad_information WHERE type = '%s'" % data).fetchall()
    ad_item = tuple_list(aditem)
    column_names = [description[0] for description in c.description]
    column = update_list(column_names, "image_name", "image_item")
    dict_data = dict_zip_multiple(ad_item, column)
    ip = socket.gethostbyname(socket.gethostname())
    for i in dict_data:
        image_path = c.execute("SELECT image_path FROM Ad_image WHERE image_name = '%s'" % i["image_item"]).fetchone()
        image_item = image_path[0]+i["image_item"]
        i["image_item"] = "http://"+ip+":8000"+image_item
    json_data = json.dumps(dict_data)
    return 200, data_good_message("获取成功", "ad_information", json_data)


def delete_ad_information(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    data = int(data)
    aditem = c.execute(f"SELECT image_name FROM Ad_information WHERE text_id = {data}").fetchone()[0]
    path = c.execute("SELECT image_path FROM Ad_image WHERE image_name = '%s'" % aditem).fetchone()[0]
    root_path = ROOT_PATH.replace("\\", "/")
    real_path = root_path + path + aditem
    c.execute("DELETE FROM Ad_information WHERE text_id ='%d'" % data)
    c.execute("DELETE FROM Ad_image WHERE image_name = '%s'" % aditem)
    os.remove(real_path)
    conn.commit()
    conn.close()
    return 200, normal_good_message("删除成功")


def update_ad_information(imagename, imagefile, data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    text_id = data["text_id"]
    title = data["title"]
    content = data["content"]
    type = data["type"]
    if imagename == "" and imagefile == "":
        c.execute(f"UPDATE Ad_information SET title={title} , content={content}, type={type} WHERE text_id={text_id}")
        conn.commit()
    else:
        image_name = c.execute(f"SELECT image_name FROM Ad_information WHERE text_id={text_id}").fetchone()[0]
        image_path = c.execute("SELECT image_path FROM Ad_image WHERE image_name='%s'"%image_name).fetchone()[0]
        root_path = ROOT_PATH.replace("\\", "/")
        real_path = root_path + image_path + image_name
        with open(real_path, 'wb') as file:
            file.write(imagefile)
        c.execute(f"UPDATE Ad_information SET title={title} , content={content}, type={type} WHERE text_id={text_id}")
        conn.commit()
    conn.commit()
    conn.close()

    return 200, normal_good_message("修改成功")
