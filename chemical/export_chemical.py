from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3
from flask import session 

export_chem_bp = Blueprint("export_chem", __name__, template_folder="templates")
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")


@export_chem_bp.route("/export_chemical", methods=["GET", "POST"])
def export_chemical():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy danh sách hóa chất
    cursor.execute("SELECT DISTINCT chemical_sap_name, unit FROM Chemicals")
    chemicals = cursor.fetchall()

    # Tính tồn kho từng loại
    inventory = {}
    for item in chemicals:
        sap = item[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_entries WHERE chemical_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_outputs WHERE chemical_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        inventory[sap] = total_in - total_out

    if request.method == "POST":
        sap_name = request.form["chemical_sap_name"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        export_date = request.form["export_date"]
        exported_by = session.get("user_name", "user lỗi")

        cursor.execute("""
            INSERT INTO Chemical_outputs (chemical_sap_name, unit, quantity, export_date, exported_by)
            VALUES (?, ?, ?, ?, ?)
        """, (sap_name, unit, quantity, export_date, exported_by))
        conn.commit()
        conn.close()
        return redirect(url_for("view_export.view_export_chemical", success="1"))

    conn.close()
    return render_template("export_chemical.html", chemicals=chemicals, inventory=inventory)
