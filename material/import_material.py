from flask import Blueprint, render_template, request, redirect
import sqlite3
import os
import uuid

# Khởi tạo Blueprint
material_bp = Blueprint("material", __name__, template_folder="templates")

# Đường dẫn chính xác đến file DB
DB_PATH = r"C:\Users\TRANG\my_app\db\my_data.db"

@material_bp.route("/import_material", methods=["GET"])
def import_material():
    # Kết nối đến cơ sở dữ liệu
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy danh sách vật tư từ bảng Materials
    materials = cursor.execute(
        "SELECT material_sap_name, unit, material_name, sap_code FROM Materials"
    ).fetchall()
    material_list = [
        {
            "material_sap_name": m[0],
            "unit": m[1],
            "material_name": m[2],
            "sap_code": m[3]
        }
        for m in materials
    ]

    # Lấy danh sách nhà cung cấp từ bảng Suppliers
    suppliers = [s[0] for s in cursor.execute("SELECT suppliers_list FROM Suppliers").fetchall()]
    conn.close()

    # Gửi dữ liệu tới template
    return render_template(
        "import_material.html",
        material_list=material_list,
        suppliers=suppliers,
        material_data=material_list
    )


from flask import Blueprint, render_template, request, redirect
import sqlite3
import uuid


@material_bp.route("/submit_material", methods=["POST"])
def submit_material():
    # Lấy dữ liệu từ form
    material_sap_names = request.form.getlist("material_sap_name[]")
    material_names = request.form.getlist("material_name[]")
    units = request.form.getlist("unit[]")
    quantities = request.form.getlist("quantity[]")
    suppliers = request.form.getlist("supplier[]")
    import_dates = request.form.getlist("import_date[]")
    sap_codes = request.form.getlist("sap_code[]")
    imported_bys = request.form.getlist("imported_by[]")

    # Sinh mã batch cho đợt nhập này
    batch_code = str(uuid.uuid4())[:8]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Duyệt từng dòng được nhập và lưu vào bảng
    for i in range(len(material_sap_names)):
        cursor.execute("""
            INSERT INTO Material_entries (
                material_sap_name, material_name, unit, quantity,
                supplier, import_date, sap_code, imported_by, batch_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            material_sap_names[i],
            material_names[i],
            units[i],
            int(quantities[i]) if quantities[i] else 0,
            suppliers[i],
            import_dates[i],
            sap_codes[i],
            imported_bys[i] if imported_bys[i] else "user tạm",
            batch_code
        ))

    conn.commit()
    conn.close()

    # Sau khi nhập, chuyển đến trang in phiếu theo batch
    return redirect(f"/print_batch/{batch_code}")


