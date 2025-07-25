from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from flask import session 

export_mat_bp = Blueprint("export_mat", __name__, template_folder="templates")
DB_PATH = r"C:\Users\TRANG\my_app\db\my_data.db"

@export_mat_bp.route("/export_material", methods=["GET", "POST"])
def export_material():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy danh sách vật tư (sap_name + unit)
    cursor.execute("SELECT DISTINCT material_sap_name, unit FROM Materials")
    materials = cursor.fetchall()

    # Tính tồn kho cho từng vật tư
    inventory_dict = {}
    for item in materials:
        sap_name = item[0]
        # Tổng nhập
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_entries WHERE material_sap_name = ?", (sap_name,))
        total_in = cursor.fetchone()[0]
        # Tổng xuất
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_outputs WHERE material_sap_name = ?", (sap_name,))
        total_out = cursor.fetchone()[0]
        inventory_dict[sap_name] = total_in - total_out

    # Xử lý submit
    if request.method == "POST":
        sap_name = request.form["material_sap_name"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        export_date = request.form["export_date"]
        exported_by = session.get("user_name", "user lỗi")

        cursor.execute("""
            INSERT INTO Material_outputs (material_sap_name, unit, quantity, export_date, exported_by)
            VALUES (?, ?, ?, ?, ?)
        """, (sap_name, unit, quantity, export_date, exported_by))
        conn.commit()
        conn.close()
        return redirect(url_for("export_mat.export_material"))

    conn.close()
    return render_template("export_material.html", materials=materials, inventory=inventory_dict)
