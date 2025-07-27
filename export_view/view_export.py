from flask import Blueprint, render_template, request, redirect, url_for
import sqlite3

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")


view_export_bp = Blueprint('view_export', __name__, template_folder="templates")

@view_export_bp.route("/view_export_material")
def view_export_material():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM Material_outputs").fetchall()
    conn.close()
    return render_template("view_export_material.html", data=rows)

@view_export_bp.route("/view_export_chemical")
def view_export_chemical():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM Chemical_outputs").fetchall()
    conn.close()
    return render_template("view_export_chemical.html", data=rows)


from flask import request  # Đảm bảo bạn đã import dòng này

@view_export_bp.route("/edit_chemical_export/<int:id>", methods=["GET", "POST"])
def edit_chemical_export(id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        sap_name = request.form["chemical_sap_name"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        export_date = request.form["export_date"]
        exported_by = request.form["exported_by"]

        cursor.execute("""
            UPDATE Chemical_outputs
            SET chemical_sap_name = ?, unit = ?, quantity = ?, export_date = ?, exported_by = ?
            WHERE id = ?
        """, (sap_name, unit, quantity, export_date, exported_by, id))
        conn.commit()
        conn.close()
        return redirect(url_for("view_export.view_export_chemical"))

    row = cursor.execute("SELECT * FROM Chemical_outputs WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit_chemical_export.html", row=row)


@view_export_bp.route("/delete_chemical_export/<int:id>")
def delete_chemical_export(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Chemical_outputs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_export.view_export_chemical"))

@view_export_bp.route("/edit_material_export/<int:id>", methods=["GET", "POST"])
def edit_material_export(id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == "POST":
        sap_name = request.form["material_sap_name"]
        unit = request.form["unit"]
        quantity = request.form["quantity"]
        export_date = request.form["export_date"]
        exported_by = request.form["exported_by"]

        cursor.execute("""
            UPDATE Material_outputs
            SET material_sap_name = ?, unit = ?, quantity = ?, export_date = ?, exported_by = ?
            WHERE id = ?
        """, (sap_name, unit, quantity, export_date, exported_by, id))
        conn.commit()
        conn.close()
        return redirect(url_for("view_export.view_export_material"))

    row = cursor.execute("SELECT * FROM Material_outputs WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("edit_material_export.html", row=row)

@view_export_bp.route("/delete_material_export/<int:id>")
def delete_material_export(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Material_outputs WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_export.view_export_material"))


