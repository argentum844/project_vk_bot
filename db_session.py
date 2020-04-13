import sqlite3
import datetime


class DataBase:
    def __init__(self):
        conn = sqlite3.connect("mydatabase.db")
        self.cursor = conn.cursor()

    def insert_request(self, user_id, text):
        date = str(datetime.datetime.now())
        sql = "SELECT enum FROM requests WHERE user_id=? AND text=?"
        self.cursor.execute(sql, [(user_id), (text)])
        print(self.cursor.fetchone())
        print(0)
db = DataBase()
db.insert_request(11, "123")
