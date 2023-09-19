import sqlite3
from datetime import datetime
from DBManager.DBConnect import connectdb
from utils.DictZip import dict_zip_multiple,dict_zip
from utils.ResponseBadMessage import bad_message
from utils.ResponseGoodMessage import normal_good_message, data_good_message
from utils.encode_decode import decrypt_string, encrypt_string


def upload_note(data):
    try:
        conn, c = connectdb()
        conn.execute('''
         CREATE TABLE IF NOT EXISTS NoteInfo (
         note_id INTEGER PRIMARY KEY AUTOINCREMENT,
         name VARCHAR,
         phone VARCHAR,
         email VARCHAR,
         note VARCHAR,
         create_time VARCHAR,
         title VARCHAR
         )
         ''')
    except Exception:
        return 400, bad_message("数据库连接失败")

    name = encrypt_string(data["name"])
    phone = encrypt_string(data["phone"])
    email = encrypt_string(data["email"])
    note = encrypt_string(data["note"])
    create_time = encrypt_string(str(datetime.now()).split(".")[0])
    title = encrypt_string(data["title"])
    tuple_data = (name, phone, email, note, create_time, title)
    c.execute("INSERT INTO NoteInfo (name, phone, email, note, create_time, title) VALUES (?,?,?,?,?,?)", tuple_data)
    conn.commit()
    conn.close()
    return 200, normal_good_message("ok")


def get_note():
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    note_item = c.execute("SELECT * FROM NoteInfo").fetchall()
    column_names = [description[0] for description in c.description]
    dict_zip = dict_zip_multiple(note_item, column_names)
    for i in dict_zip:
        for k,v in i.items():
            if k == "note_id":
                continue
            i[k] = decrypt_string(v)
    return 200, data_good_message("获取成功", "note_information", dict_zip)


def update_note(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    note_id = data["note_id"]
    key = []
    value = []
    for k, v in data.items():
        if k == "note_id":
            continue
        key.append(k)
        value.append(encrypt_string(v))

    update_query = "UPDATE NoteInfo SET "
    count = 0
    for i in range(len(key) - 1):
        update_query += f"{key[count]} = '{value[count]}', "
        count += 1
    update_query += f"{key[count]} = '{value[count]}' WHERE note_id ={note_id}"
    c.execute(update_query)
    conn.commit()
    conn.close()
    return 200, normal_good_message("修改成功")


def delete_note(data):
    try:
        conn, c = connectdb()
    except Exception:
        return 400, bad_message("数据库连接失败")

    note_id = data["note_id"]
    c.execute(f"DELETE FROM NoteInfo WHERE note_id={note_id}")
    conn.commit()
    conn.close()
    return 200, normal_good_message("删除成功")