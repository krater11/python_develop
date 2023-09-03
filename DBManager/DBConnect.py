import sqlite3
from settings import DATABASE


def connectdb():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    return conn, c