import sqlite3
import datetime


class DataBase:
    def __init__(self, text, user_id):
        self.conn = sqlite3.connect("mydatabase.db")
        self.cursor = self.conn.cursor()
        self.user_id = user_id
        self.text = text

    def insert_request(self):
        date = str(datetime.datetime.now())
        sql = "INSERT INTO requests VALUES (?,?,?)"
        print(f'user_id={self.user_id}\ntext={self.text}\ndate={date}\n\n')
        self.cursor.execute(sql, [self.user_id, self.text, date])
        self.conn.commit()

    def get_requests(self, is_user_id):
        if is_user_id:
            sql = "SELECT text FROM requests WHERE user_id=?"
            self.cursor.execute(sql, [self.user_id])
        else:
            sql = "SELECT text FROM requests"
            self.cursor.execute(sql)
        return self.cursor.fetchall()

