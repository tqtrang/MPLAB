from flask import Blueprint, render_template, request
import sqlite3

log_mat_bp = Blueprint("log_mat", __name__, template_folder="templates")
DB_PATH = r"C:\Users\TRANG\my_app\db\my_data.db"

@log_mat_bp.route("/log_material", methods=["GET", "POST"])
def log_material():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy danh sách tên vật tư để chọn
    cursor.execute("SELECT DISTINCT material_name FROM Material_entries")
    name_list = [row[0] for row in cursor.fetchall()]

    logs = []
    selected = None

    if request.method == "POST":
        selected = request.form["material_name"]
        cursor.execute("""
            SELECT import_date, material_sap_name, unit, quantity, supplier, imported_by
            FROM Material_entries
            WHERE material_name = ?
            ORDER BY import_date DESC
        """, (selected,))
        logs = cursor.fetchall()

    conn.close()
    return render_template("log_material.html", name_list=name_list, logs=logs, selected=selected)
