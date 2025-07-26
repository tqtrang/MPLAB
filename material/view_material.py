from flask import Blueprint, render_template,request, redirect
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")

view_bp = Blueprint("view_mat", __name__, template_folder="templates")


@view_bp.route("/view_material")
def view_material():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Material_entries ORDER BY import_date DESC")
    rows = cursor.fetchall()

    # Lấy tên cột
    col_names = [description[0] for description in cursor.description]
    conn.close()

    return render_template("view_material.html", rows=rows, col_names=col_names)

@view_bp.route("/edit_material/<int:entry_id>", methods=["GET"])
def edit_material(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Material_entries WHERE id = ?", (entry_id,))
    entry = cursor.fetchone()

    # Lấy danh sách vật tư SAP và nhà cung cấp để chỉnh sửa
    materials = cursor.execute(
        "SELECT material_sap_name FROM Materials"
    ).fetchall()
    suppliers = cursor.execute(
        "SELECT suppliers_list FROM Suppliers"
    ).fetchall()
    conn.close()

    return render_template("edit_material.html",
                           entry=entry,
                           material_sap_list=[m[0] for m in materials],
                           supplier_list=[s[0] for s in suppliers])

@view_bp.route("/edit_material/<int:entry_id>", methods=["POST"])
def update_material(entry_id):
    data = {
        "material_sap_name": request.form["material_sap_name"],
        "material_name": request.form["material_name"],
        "unit": request.form["unit"],
        "quantity": int(request.form["quantity"]),
        "supplier": request.form["supplier"],
        "import_date": request.form["import_date"],
        "sap_code": request.form["sap_code"],
        "imported_by": request.form["imported_by"]
    }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Material_entries SET
            material_sap_name = ?, material_name = ?, unit = ?, quantity = ?,
            supplier = ?, import_date = ?, sap_code = ?, imported_by = ?
        WHERE id = ?
    """, (*data.values(), entry_id))

    conn.commit()
    conn.close()

    return redirect("/view_material")

@view_bp.route("/delete_material/<int:entry_id>", methods=["POST"])
def delete_material(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Material_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()

    return redirect("/view_material")

@view_bp.route("/print_material/<int:entry_id>")
def print_material(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Material_entries WHERE id = ?", (entry_id,))
    entry = cursor.fetchone()
    conn.close()

    return render_template("print_material.html", entry=entry)

@view_bp.route("/print_batch/<batch_code>")
def print_batch(batch_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Thử lấy từ bảng vật tư
    cursor.execute("""
        SELECT id, material_sap_name, unit, quantity, sap_code, imported_by, import_date
        FROM Material_entries WHERE batch_code = ?
    """, (batch_code,))
    rows = cursor.fetchall()

    if rows:
        imported_by = rows[0][5]
        import_date = rows[0][6]
        data_type = "material"
    else:
        # Nếu không có vật tư, thử bảng hoá chất
        cursor.execute("""
            SELECT id, chemical_sap_name, unit, quantity, sap_code, imported_by, import_date
            FROM Chemical_entries WHERE batch_code = ?
        """, (batch_code,))
        rows = cursor.fetchall()

        if rows:
            imported_by = rows[0][5]
            import_date = rows[0][6]
            data_type = "chemical"
        else:
            conn.close()
            return "Không tìm thấy phiếu nhập cho batch này"

    conn.close()

    return render_template("print_batch.html",
                           rows=rows,
                           batch_code=batch_code,
                           imported_by=imported_by,
                           import_date=import_date,
                           data_type=data_type)



