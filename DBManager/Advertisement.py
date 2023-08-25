import uuid

from DBManager.DBConnect import connectdb
from settings import ROOT_PATH, IMAGE_PATH
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import data_good_message, normal_good_message


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
        image_name VARCHAR REFERENCES Ad_image (image_name))''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    title = data["title"]
    titleitem = c.execute("SELECT text_id FROM Ad_information WHERE title = '%s'" % title).fetchone()
    if titleitem is not None:
        return 400, bad_message("title已存在")
    content = data["content"]
    root_path = ROOT_PATH.replace("\\", "/")
    file_type = imagename.split(".")[-1]
    generate_uuid = uuid.uuid4()
    name_list = [str(generate_uuid), file_type]
    imagefile_name = ".".join(name_list)
    image_path = IMAGE_PATH + "/" + "ad_image"
    image_data = (imagefile_name, image_path)
    information_data = (title, content, imagefile_name)
    with open(root_path+image_path+imagefile_name, 'wb') as f:
        f.write(imagefile)
    c.execute("INSERT INTO Ad_image (image_name, image_path) VALUES (?, ?)", image_data)
    c.execute("INSERT INTO Ad_information (title, content, image_name) VALUES (?, ?, ?)", information_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("上传成功")