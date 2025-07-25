import pandas as pd
import sqlite3

# Đường dẫn file
excel_path = "C:/Users/TRANG/my_app/db/OLD DATA.xlsx"
db_path = "C:/Users/TRANG/my_app/db/my_data.db"

# Đọc dữ liệu từ Excel
df_chemical = pd.read_excel(excel_path, sheet_name="Chemical_entries")
df_material = pd.read_excel(excel_path, sheet_name="Material_entries")

# Kết nối đến database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ✅ Cập nhật Chemical_entries
for _, row in df_chemical.iterrows():
    # Xử lý ngày theo định dạng chuẩn
    import_date_parsed = pd.to_datetime(row['import_date'], format='%Y-%m-%d', errors='coerce')
    expiration_date_parsed = pd.to_datetime(row['expiration_date'], format='%Y-%m-%d', errors='coerce')

    import_date_str = import_date_parsed.strftime('%Y-%m-%d') if pd.notnull(import_date_parsed) else None
    expiration_date_str = expiration_date_parsed.strftime('%Y-%m-%d') if pd.notnull(expiration_date_parsed) else None

    cursor.execute("""
        UPDATE Chemical_entries SET
            chemical_sap_name = ?, chemical_name = ?, unit = ?, quantity = ?,
            supplier = ?, import_date = ?, sap_code = ?, lot_number = ?,
            storage_condition = ?, expiration_date = ?, imported_by = ?, batch_code = ?
        WHERE id = ?;
    """, (
        str(row['chemical_sap_name']),
        str(row['chemical_name']),
        str(row['unit']),
        row['quantity'],
        str(row['supplier']),
        import_date_str,
        str(row['sap_code']),
        str(row['lot_number']),
        str(row['storage_condition']),
        expiration_date_str,
        str(row['imported_by']),
        str(row['batch_code']),
        row['id']
    ))

# ✅ Cập nhật Material_entries
for _, row in df_material.iterrows():
    # Xử lý ngày
    import_date_parsed = pd.to_datetime(row['import_date'], format='%Y-%m-%d', errors='coerce')
    import_date_str = import_date_parsed.strftime('%Y-%m-%d') if pd.notnull(import_date_parsed) else None

    cursor.execute("""
        UPDATE Material_entries SET
            material_sap_name = ?, material_name = ?, unit = ?, quantity = ?,
            supplier = ?, import_date = ?, sap_code = ?, imported_by = ?, batch_code = ?
        WHERE id = ?;
    """, (
        str(row['material_sap_name']),
        str(row['material_name']),
        str(row['unit']),
        row['quantity'],
        str(row['supplier']),
        import_date_str,
        str(row['sap_code']),
        str(row['imported_by']),
        str(row['batch_code']),
        row['id']
    ))

# Lưu và đóng kết nối
conn.commit()
conn.close()


