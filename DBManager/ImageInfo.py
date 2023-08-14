import base64
import os.path
import sqlite3
from settings import DATABASE, IMAGE_PATH, ROOT_PATH


def UploadImage(image_file, image_name):
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 401, "链接失败"

    item = c.execute("SELECT image_name FROM ImageInfo WHERE image_name = '%s'" % image_name)
    imageitem = item.fetchone()
    if imageitem is not None:
        c.close()
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
        c.close()
        conn.close()
    except Exception:
        c.close()
        conn.close()
        return 400, "上传失败"

    return 200, "上传成功"


def GetImage(image_name):
    try:
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
    except Exception:
        return 400, "数据库连接失败"

    item = c.execute("SELECT image_name FROM ImageInfo WHERE image_name = '%s'" % image_name)
    imageitem = item.fetchone()

    if imageitem is None:
        conn.close()
        return 400, "图片不存在"

    item1 = c.execute("SELECT image_file FROM ImageInfo WHERE image_name = '%s'" % image_name)
    imageitem1 = item1.fetchone()
    root_path = ROOT_PATH.replace("\\", "/")
    path = root_path + imageitem1[0] + "/" + image_name
    conn.close()
    return 200, path
