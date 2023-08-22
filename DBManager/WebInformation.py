import sqlite3
from settings import DATABASE
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message


def upload_webinformation(data):

    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
    except Exception:
        return 400, bad_message("服务器连接失败")

    conn.execute('''
    CREATE TABLE IF NOT EXISTS WebInformation (    web_name     VARCHAR,
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
    amazon_url   VARCHAR)''')

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
    tuple_data = (web_name, web_ip, phone, email, postal_code, location, seo_key, seo_des, work_time, facebook_url, twitter_url, youtube_url, google_url, amazon_url)
    information = c.execute("SELECT web_name FROM WebInformation WHERE web_name = '%s'" % web_name).fetchone()
    if information is not None:
        return 400, "名称已存在"
    c.execute("INSERT INTO WebInformation (web_name, web_ip, phone, email, postal_code, location, seo_key, seo_des, work_time, facebook_url, twitter_url, youtube_url, google_url, amazon_url)"
              " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tuple_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("ok")