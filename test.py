import sqlite3

DB_PATH = r"C:\Users\TRANG\my_app\db\my_data.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
