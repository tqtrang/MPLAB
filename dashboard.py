from flask import Blueprint, render_template
import sqlite3
from datetime import date
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "my_data.db")

print("📂 Đường dẫn database đang dùng:", DB_PATH)

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard")
def index():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    low_stock_alerts = []

    # Kiểm tra tồn kho vật tư
    cursor.execute("SELECT material_sap_name, unit, COALESCE(min_material, 0) FROM Materials")
    for sap, unit, min_q in cursor.fetchall():
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_entries WHERE material_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_outputs WHERE material_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton <= min_q:
            low_stock_alerts.append(1)

    # Kiểm tra tồn kho hóa chất
    cursor.execute("SELECT chemical_sap_name, unit, COALESCE(min_chemical, 0) FROM Chemicals")
    for sap, unit, min_q in cursor.fetchall():
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_entries WHERE chemical_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_outputs WHERE chemical_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton <= min_q:
            low_stock_alerts.append(1)

    alert_count = len(low_stock_alerts)
    conn.close()

    return render_template("dashboard.html", alert_count=alert_count)



@dashboard_bp.route("/import_menu")
def import_menu():
    return render_template("import_menu.html")


@dashboard_bp.route("/export_menu")
def export_menu():
    return render_template("export_menu.html")


@dashboard_bp.route("/statistic_menu")
def statistic_menu():
    return render_template("statistic_menu.html")


@dashboard_bp.route("/dashboard/notifications")
def notifications():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = date.today().isoformat()

    # Kiểm tra có nhập
    cursor.execute("SELECT COUNT(*) FROM Material_entries WHERE import_date = ?", (today,))
    mat_in = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Chemical_entries WHERE import_date = ?", (today,))
    chem_in = cursor.fetchone()[0]
    has_import_today = (mat_in + chem_in) > 0

    # Kiểm tra có xuất
    cursor.execute("SELECT COUNT(*) FROM Material_outputs WHERE export_date = ?", (today,))
    mat_out = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM Chemical_outputs WHERE export_date = ?", (today,))
    chem_out = cursor.fetchone()[0]
    has_export_today = (mat_out + chem_out) > 0

    # Cảnh báo tồn kho thấp
    low_stock_alerts = []

    cursor.execute("SELECT material_sap_name, unit, COALESCE(min_material, 0) FROM Materials")
    for sap, unit, min_q in cursor.fetchall():
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_entries WHERE material_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Material_outputs WHERE material_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton <= min_q:
            low_stock_alerts.append(f"[Vật tư] {sap} còn {ton} {unit} (giới hạn {min_q})")

    cursor.execute("SELECT chemical_sap_name, unit, COALESCE(min_chemical, 0) FROM Chemicals")
    for sap, unit, min_q in cursor.fetchall():
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_entries WHERE chemical_sap_name = ?", (sap,))
        total_in = cursor.fetchone()[0]
        cursor.execute("SELECT COALESCE(SUM(quantity), 0) FROM Chemical_outputs WHERE chemical_sap_name = ?", (sap,))
        total_out = cursor.fetchone()[0]
        ton = total_in - total_out
        if ton <= min_q:
            low_stock_alerts.append(f"[Hóa chất] {sap} còn {ton} {unit} (giới hạn {min_q})")

    conn.close()

    return render_template("notifications.html",
                           has_import_today=has_import_today,
                           has_export_today=has_export_today,
                           low_stock_alerts=low_stock_alerts)
