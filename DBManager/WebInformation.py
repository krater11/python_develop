import base64
import json
import sqlite3
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import data_good_message
from DBManager.DBConnect import connectdb
from settings import DATABASE
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message
from utils.DictZip import dict_zip


def upload_webinformation(file, data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS WebInformation (
    web_id INTEGER PRIMARY KEY AUTOINCREMENT,
    web_name     VARCHAR,
    web_ip       VARCHAR,
    phone        INTEGER,
    email        VARCHAR,
    postal_code  VARCHAR,
    location     VARCHAR,
    seo_key      VARCHAR,
    seo_des      VARCHAR,
    work_time    DATETIME,
    facebook_url VARCHAR,
    twitter_url  VARCHAR,
    youtube_url  VARCHAR,
    google_url   VARCHAR,
    amazon_url   VARCHAR,
    logo_image   VARCHAR)''')
    web_name = data["web_name"]
    web_ip = data["web_ip"]
    phone = data["phone"]
    email = data["email"]
    postal_code = data["postal_code"]
    location = data["location"]
    seo_key = data["seo_key"]
    seo_des = data["seo_des"]
    work_time = data["work_time"]
    facebook_url = data["facebook_url"]
    twitter_url = data["twitter_url"]
    youtube_url = data["youtube_url"]
    google_url = data["google_url"]
    amazon_url = data["amazon_url"]
    tuple_data = (web_name, web_ip, phone, email, postal_code, location, seo_key, seo_des, work_time, facebook_url, twitter_url, youtube_url, google_url, amazon_url, file[0])
    information = c.execute("SELECT web_name FROM WebInformation WHERE web_id=1").fetchone()
    if information is not None:
        c.execute("UPDATE WebInformation SET web_name=?, web_ip=?, phone=?, email=?, postal_code=?, location=?, seo_key=?, seo_des=?, work_time=?, facebook_url=?, twitter_url=?, youtube_url=?, google_url=?, amazon_url=? WHERE web_id=1", tuple_data[:-1])
        if file[0] == "null":
            conn.commit()
            conn.close()
            return 200, normal_good_message("修改成功")
        c.execute("UPDATE WebInformation SET logo_image=? WHERE web_id=1", [(file[0])])
        conn.commit()
        conn.close()
        return 200, normal_good_message("修改成功")
    sql = "INSERT INTO WebInformation (web_name, web_ip, phone, email, postal_code, location, seo_key, seo_des, work_time, facebook_url, twitter_url, youtube_url, google_url, amazon_url, logo_image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    c.execute(sql, tuple_data)
    conn.commit()
    conn.commit()
    conn.close()
    return 200, normal_good_message("ok")


def get_web_information():
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")
    infoitem = c.execute("SELECT * FROM WebInformation WHERE web_id = 1").fetchone()
    column_names = [description[0] for description in c.description]
    zip_data = dict_zip(infoitem, column_names)
    zip_data["logo_image"] = base64.b64encode(zip_data["logo_image"]).decode("utf-8")
    json_data = json.dumps(zip_data)
    conn.close()
    return 200, data_good_message("获取成功", "web_information", json_data)