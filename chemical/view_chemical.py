from flask import Blueprint, render_template, request, redirect
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")


view_chem_bp = Blueprint("view_chem", __name__, template_folder="templates")


@view_chem_bp.route("/view_chemical")
def view_chemical():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Chemical_entries ORDER BY import_date DESC")
    rows = cursor.fetchall()
    col_names = [desc[0] for desc in cursor.description]
    conn.close()
    return render_template("view_chemical.html", rows=rows, col_names=col_names)


@view_chem_bp.route("/edit_chemical/<int:entry_id>", methods=["GET"])
def edit_chemical(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Chemical_entries WHERE id = ?", (entry_id,))
    entry = cursor.fetchone()

    chemicals = cursor.execute("SELECT chemical_sap_name FROM Chemicals").fetchall()
    suppliers = cursor.execute("SELECT suppliers_list FROM Suppliers").fetchall()

    conn.close()
    return render_template("edit_chemical.html",
                           entry=entry,
                           chemical_sap_list=[c[0] for c in chemicals],
                           supplier_list=[s[0] for s in suppliers])


@view_chem_bp.route("/edit_chemical/<int:entry_id>", methods=["POST"])
def update_chemical(entry_id):
    data = {
        "chemical_sap_name": request.form["chemical_sap_name"],
        "chemical_name": request.form["chemical_name"],
        "unit": request.form["unit"],
        "quantity": int(request.form["quantity"]),
        "supplier": request.form["supplier"],
        "import_date": request.form["import_date"],
        "sap_code": request.form["sap_code"],
        "lot_number": request.form["lot_number"],
        "storage_condition": request.form["storage_condition"],
        "expiration_date": request.form["expiration_date"],
        "imported_by": request.form["imported_by"]
    }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Chemical_entries SET
            chemical_sap_name = ?, chemical_name = ?, unit = ?, quantity = ?,
            supplier = ?, import_date = ?, sap_code = ?, lot_number = ?,
            storage_condition = ?, expiration_date = ?, imported_by = ?
        WHERE id = ?
    """, (*data.values(), entry_id))

    conn.commit()
    conn.close()
    return redirect("/view_chemical")


@view_chem_bp.route("/delete_chemical/<int:entry_id>", methods=["POST"])
def delete_chemical(entry_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Chemical_entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()
    return redirect("/view_chemical")
