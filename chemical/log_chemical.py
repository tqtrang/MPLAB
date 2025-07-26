from flask import Blueprint, render_template, request
import sqlite3
from urllib.parse import unquote

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")


log_chem_bp = Blueprint("log_chem", __name__, template_folder="templates")


@log_chem_bp.route("/log_chemical", methods=["GET", "POST"])
def log_chemical():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy danh sách chemical_name để làm dropdown
    cursor.execute("SELECT DISTINCT chemical_name FROM Chemical_entries")
    name_list = [row[0] for row in cursor.fetchall()]

    logs = []
    selected = None

    if request.method == "POST":
        selected = request.form["chemical_name"]
        cursor.execute("""
            SELECT import_date, chemical_sap_name, unit, quantity, lot_number, expiration_date, supplier, imported_by
            FROM Chemical_entries
            WHERE chemical_name = ?
            ORDER BY import_date DESC
        """, (selected,))
        logs = cursor.fetchall()

    conn.close()
    return render_template("log_chemical.html", name_list=name_list, logs=logs, selected=selected)



@log_chem_bp.route("/print_log_chemical/<path:chemical_encoded>")
def print_log_chemical(chemical_encoded):
    chemical_name = unquote(chemical_encoded)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy toàn bộ lịch sử nhập của hóa chất
    cursor.execute("""
        SELECT import_date, quantity, lot_number, supplier, unit, imported_by, expiration_date
        FROM Chemical_entries
        WHERE chemical_name = ?
        ORDER BY import_date ASC
    """, (chemical_name,))
    logs = cursor.fetchall()

    # Lấy 1 dòng để truy xuất điều kiện bảo quản
    cursor.execute("""
        SELECT storage_condition
        FROM Chemical_entries
        WHERE chemical_name = ?
        LIMIT 1
    """, (chemical_name,))
    row = cursor.fetchone()
    storage = row[0] if row else "________"

    # Thông tin placeholder chưa có
    formula = "________"
    warning = "Không được đưa lên mắt, lên da, hoặc lên quần áo."

    conn.close()

    return render_template("print_log_chemical.html",
                           chemical_name=chemical_name,
                           logs=logs,
                           formula=formula,
                           storage=storage,
                           warning=warning)


