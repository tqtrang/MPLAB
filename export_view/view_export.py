from flask import Blueprint, render_template
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
