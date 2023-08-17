import json
import os
import sqlite3
from utils.DictZip import dict_zip_multiple
from settings import DATABASE, IMAGE_PATH, ROOT_PATH


def UploadImage(imagefile, imagename):
    try:
        conn = sqlite3.connect(DATABASE)
        conn.execute('''
        CREATE TABLE IF NOT EXISTS ImageInfo (
        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_file VARCHAR (255),
        image_name VARCHAR)''')
        c = conn.cursor()
    except Exception:
        return 401, "链接失败"

    count = 0
    for i in imagename:
        image_file = imagefile[count]
        image_name = imagename[count]
        item = c.execute("SELECT image_name FROM ImageInfo WHERE image_name = '%s'" % image_name)
        imageitem = item.fetchone()
        if imageitem is not None:
            conn.close()
            return 401, "图片名称已存在请更改名称后重新上传"
        root_path = ROOT_PATH.replace("\\", "/")
        file_path = root_path + IMAGE_PATH + "/" + image_name
        image_data = (IMAGE_PATH, image_name)
        try:
            with open(file_path, 'wb') as f:
                f.write(image_file)
            c.execute("INSERT INTO ImageInfo (image_file, image_name) VALUES(?, ?)", image_data)
            conn.commit()
        except Exception:
            conn.close()
            return 400, "上传失败"

        count += 1
    conn.close()

    return 200, "上传成功"


def GetImage(imagename):
    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "数据库连接失败"

    path_list = []
    for image_name in imagename:
        item = c.execute("SELECT image_name FROM ImageInfo WHERE image_name = '%s'" % image_name)
        imageitem = item.fetchone()

        if imageitem is None:
            conn.close()
            return 400, "图片不存在"

        item1 = c.execute("SELECT image_file FROM ImageInfo WHERE image_name = '%s'" % image_name)
        imageitem1 = item1.fetchone()
        root_path = ROOT_PATH.replace("\\", "/")
        path = root_path + imageitem1[0] + "/" + image_name
        path_list.append(path)
    conn.close()
    return 200, path_list


def GetImageList():
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, "数据库连接失败"

    imageitem = c.execute("SELECT * FROM ImageInfo").fetchall()
    column_names = [description[0] for description in c.description]
    dictzip = dict_zip_multiple(imageitem, column_names)
    json_dict = json.dumps(dictzip)
    return 200, json_dict


def DeleteImage(image_name):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, "数据库连接失败"


    imageitem = c.execute("SELECT image_file FROM ImageInfo WHERE image_name = '%s'" % image_name).fetchone()
    if imageitem is None:
        conn.close()
        return 400, "照片不存在"

    root_path = ROOT_PATH.replace("\\", "/")
    path = root_path + imageitem[0] + "/" + image_name
    os.remove(path)
    c.execute("DELETE FROM ImageInfo WHERE image_name = '%s'" % image_name)
    conn.commit()
    conn.close()

    return 200, "照片删除成功"
