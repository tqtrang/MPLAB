import sqlite3
import os

def run():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tạo user admin nếu chưa tồn tại
    cursor.execute("SELECT * FROM Users WHERE user_id = ?", ('admin',))
    if cursor.fetchone():
        print("👤 User 'admin' đã tồn tại.")
    else:
        cursor.execute("""
            INSERT INTO Users (user_id, user_name, role, password)
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin', 'admin', 'admin'))
        conn.commit()
        print("✅ Đã thêm user 'admin'.")

    conn.close()
