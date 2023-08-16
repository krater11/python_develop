import sqlite3
from settings import DATABASE


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
        return 400, "连接失败"
    text_name = data["text_name"]
    text = data["text"]
    text_font = data["text_font"]
    text_color = data["text_color"]
    text_bold = data["text_bold"]
    text_italic = data["text_italic"]
    text_data = tuple([text_name, text, text_font, text_color, text_bold, text_italic])
    textitem = c.execute("SELECT text_id FROM RichTextInfo WHERE text_name = '%s'" % text_name).fetchone()
    if textitem is not None:
        return 400, "文本名重复"

    try:
        c.execute("INSERT INTO RichTextInfo (text_name, text, text_font, text_color, text_bold, text_italic) VALUES (?, ?, ?, ?, ?, ?)", text_data)
        conn.commit()
        conn.close()
    except Exception:
        print(Exception)
    return 200, "保存成功"