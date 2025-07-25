import sqlite3
import pandas as pd

# Đường dẫn tới file Excel & DB
excel_path = r"C:\Users\TRANG\my_app\Data_user.xlsx"  # Cập nhật nếu khác
db_path = r"C:\Users\TRANG\my_app\db\my_data.db"

# Đọc Excel
df = pd.read_excel(excel_path)

# Kết nối DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Xoá dữ liệu cũ nếu muốn (tuỳ chọn)
# cursor.execute("DELETE FROM Users")

# Ghi dữ liệu
for _, row in df.iterrows():
    cursor.execute("INSERT OR REPLACE INTO Users (user_id, user_name) VALUES (?, ?)",
                   (row['user_id'], row['user_name']))

conn.commit()
conn.close()
print("✅ Đã import danh sách user vào DB.")
