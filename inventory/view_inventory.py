from flask import Blueprint, render_template, send_file
import sqlite3
import pandas as pd
import io

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")


inventory_bp = Blueprint("inventory", __name__, template_folder="templates")


# ====== TRANG TỒN KHO CHÍNH ======
@inventory_bp.route("/inventory")
def view_inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # -------- TỒN KHO VẬT TƯ --------
    cursor.execute("SELECT DISTINCT material_sap_name, unit FROM Materials")
    materials = cursor.fetchall()
    material_data = []
    for sap, unit in materials:
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_entries WHERE material_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_outputs WHERE material_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton > 0:
            material_data.append((sap, unit, ton))

    # -------- TỒN KHO HÓA CHẤT --------
    cursor.execute("SELECT DISTINCT chemical_sap_name, unit FROM Chemicals")
    chemicals = cursor.fetchall()
    chemical_data = []
    for sap, unit in chemicals:
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_entries WHERE chemical_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_outputs WHERE chemical_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton > 0:
            chemical_data.append((sap, unit, ton))

    conn.close()
    return render_template("inventory.html",
                           material_data=material_data,
                           chemical_data=chemical_data)

# ====== XUẤT FILE EXCEL ======
@inventory_bp.route("/export_inventory_excel")
def export_excel():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # VẬT TƯ
    cursor.execute("SELECT DISTINCT material_sap_name, unit FROM Materials")
    materials = cursor.fetchall()
    mat_rows = []
    for sap, unit in materials:
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_entries WHERE material_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_outputs WHERE material_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton > 0:
            mat_rows.append({"Tên vật tư (SAP)": sap, "Đơn vị tính": unit, "Số lượng tồn": ton})

    # HÓA CHẤT
    cursor.execute("SELECT DISTINCT chemical_sap_name, unit FROM Chemicals")
    chemicals = cursor.fetchall()
    chem_rows = []
    for sap, unit in chemicals:
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_entries WHERE chemical_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_outputs WHERE chemical_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton > 0:
            chem_rows.append({"Tên hóa chất (SAP)": sap, "Đơn vị tính": unit, "Số lượng tồn": ton})

    conn.close()

    # Ghi vào file Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame(mat_rows).to_excel(writer, index=False, sheet_name="Vật tư")
        pd.DataFrame(chem_rows).to_excel(writer, index=False, sheet_name="Hóa chất")

    output.seek(0)
    return send_file(output, download_name="Ton_kho.xlsx", as_attachment=True)


@inventory_bp.route("/inventory/print")
def print_inventory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy dữ liệu vật tư
    cursor.execute("SELECT DISTINCT material_sap_name, unit FROM Materials")
    materials = cursor.fetchall()
    material_data = []
    for sap, unit in materials:
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_entries WHERE material_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_outputs WHERE material_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton > 0:
            material_data.append((sap, unit, ton))

    # Lấy dữ liệu hóa chất
    cursor.execute("SELECT DISTINCT chemical_sap_name, unit FROM Chemicals")
    chemicals = cursor.fetchall()
    chemical_data = []
    for sap, unit in chemicals:
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_entries WHERE chemical_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_outputs WHERE chemical_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton > 0:
            chemical_data.append((sap, unit, ton))

    conn.close()
    return render_template("inventory_print.html", material_data=material_data, chemical_data=chemical_data)
