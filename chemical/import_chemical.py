from flask import Blueprint, render_template, request, redirect
import sqlite3
import uuid
import os

chemical_bp = Blueprint("chemical", __name__, template_folder="templates")

DB_PATH = r"C:\Users\TRANG\my_app\db\my_data.db"

@chemical_bp.route("/import_chemical", methods=["GET"])
def import_chemical():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Lấy danh sách hoá chất từ bảng Chemicals
    chemicals = cursor.execute(
        "SELECT chemical_sap_name, unit, chemical_name, sap_code FROM Chemicals"
    ).fetchall()
    chemical_list = [
        {
            "chemical_sap_name": c[0],
            "unit": c[1],
            "chemical_name": c[2],
            "sap_code": c[3]
        }
        for c in chemicals
    ]

    # Lấy danh sách nhà cung cấp từ bảng Suppliers
    suppliers = [s[0] for s in cursor.execute("SELECT suppliers_list FROM Suppliers").fetchall()]
    conn.close()

    return render_template(
        "import_chemical.html",
        chemical_data=chemical_list,
        suppliers=suppliers
    )


@chemical_bp.route("/submit_chemical", methods=["POST"])
def submit_chemical():
    # Lấy dữ liệu từ form
    chemical_sap_names = request.form.getlist("chemical_sap_name[]")
    chemical_names = request.form.getlist("chemical_name[]")
    units = request.form.getlist("unit[]")
    quantities = request.form.getlist("quantity[]")
    suppliers = request.form.getlist("supplier[]")
    import_dates = request.form.getlist("import_date[]")
    sap_codes = request.form.getlist("sap_code[]")
    lot_numbers = request.form.getlist("lot_number[]")
    storage_conditions = request.form.getlist("storage_condition[]")
    expiration_dates = request.form.getlist("expiration_date[]")
    imported_bys = request.form.getlist("imported_by[]")

    batch_code = str(uuid.uuid4())[:8]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for i in range(len(chemical_sap_names)):
        cursor.execute("""
            INSERT INTO Chemical_entries (
                chemical_sap_name, chemical_name, unit, quantity,
                supplier, import_date, sap_code, lot_number,
                storage_condition, expiration_date, imported_by, batch_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chemical_sap_names[i],
            chemical_names[i],
            units[i],
            int(quantities[i]) if quantities[i] else 0,
            suppliers[i],
            import_dates[i],
            sap_codes[i],
            lot_numbers[i],
            storage_conditions[i],
            expiration_dates[i],
            imported_bys[i] if imported_bys[i] else "user tạm",
            batch_code
        ))

    conn.commit()
    conn.close()

    return redirect(f"/print_batch/{batch_code}")  # sử dụng lại phiếu in giống vật tư
