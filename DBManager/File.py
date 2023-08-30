import os
import socket
import sqlite3
import uuid
from pathlib import Path
from DBManager.DBConnect import connectdb
from settings import ROOT_PATH, FILE_PATH, PORT
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import data_good_message, normal_good_message

root_path = ROOT_PATH.replace("\\", "/")
file_path = FILE_PATH + "/file_zip"


def upload_file(imagename, imagefile):
    try:
        conn,c = connectdb()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS File_zip (
        file_id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name VARCHAR,
        file_path VARCHAR)''')
    except Exception:
        return 400, bad_message("数据库连接失败")
    real_path = root_path + file_path
    Path(real_path.replace("/", "\\")).mkdir(parents=True, exist_ok=True)
    count = 0
    data = []
    ip = socket.gethostbyname(socket.gethostname())
    for i in imagename:
        file_type = i.split(".")[-1]
        generate_uuid = uuid.uuid4()
        name_list = [str(generate_uuid), file_type]
        imagefile_name = ".".join(name_list)

        with open(real_path + "/" + imagefile_name, 'wb') as f:
            f.write(imagefile[count])
        image_data = (imagefile_name, file_path)
        c.execute("INSERT INTO Image_zip (image_name, image_path) VALUES (?, ?)", image_data)
        count += 1
        url = f"http://{ip}:{PORT}{file_path}/{imagefile_name}"
        data.append(url)
    conn.commit()
    conn.close()
    return 200, data_good_message("上传成功", "image", data)


def delete_file(data):
    try:
        conn,c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    url = data["url"]
    url_list = url.split(",")
    for i in url_list:
        detail_list = i.split("/")
        if detail_list[-2] != "image_zip":
            return 400, bad_message("url错误")
        file_name = detail_list[-1]
        file_path = c.execute("SELECT file_path FROM File_zip WHERE file_name='%s'" % file_name).fetchone()[0]
        detail_path = root_path + file_path + "/" + file_name
        os.remove(detail_path)
        c.execute("DELETE FROM File_zip WHERE file_name ='%s'" % file_name)
    conn.commit()
    conn.close()

    return 200, normal_good_message("删除成功")