import sqlite3
from DBManager.DBConnect import connectdb


def find_subset(superset):
    try:
        conn, c = connectdb()
    except Exception:
        print("error")

    item = c.execute(f"SELECT name,type FROM {superset}").fetchall()

    return item