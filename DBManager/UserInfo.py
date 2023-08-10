import sqlite3


try:
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
except Exception:
    print("连接失败")


def UserRegist():


    item = c.execute("SELECT * from UserInfo WHERE user_name = "+ username)

    return


def UserLogin():

    return