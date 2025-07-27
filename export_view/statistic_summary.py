from flask import Blueprint, render_template, request, send_file
import sqlite3
import pandas as pd
import io
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")

statistic_summary_bp = Blueprint("statistic_summary", __name__, template_folder="templates")

@statistic_summary_bp.route("/statistics/summary", methods=["GET", "POST"])
def summary():
    # Lấy thông tin từ form
    mode = request.form.get("mode", "month")
    month = request.form.get("month", "07")
    year = request.form.get("year", "2025")
    item_type = request.form.get("item_type", "chemical")
    action_type = request.form.get("action_type", "import")

    month = month.zfill(2)  # Đảm bảo tháng luôn có 2 chữ số

    if item_type == "material":
        entry_table = "Material_entries"
        output_table = "Material_outputs"
        name_table = "Materials"
        sap_name_col = "material_sap_name"
        name_col = "material_name"
    else:
        entry_table = "Chemical_entries"
        output_table = "Chemical_outputs"
        name_table = "Chemicals"
        sap_name_col = "chemical_sap_name"
        name_col = "chemical_name"

    conn = sqlite3.connect(DB_PATH)

    # Truy vấn chính
    if action_type == "import":
        date_field = "import_date"
        source_table = entry_table
    else:
        date_field = "export_date"
        source_table = output_table

    if mode == "month":
        query = f"""
            SELECT {sap_name_col} as sap_name, SUM(quantity) as total_qty
            FROM {source_table}
            WHERE strftime('%Y', {date_field}) = ? AND strftime('%m', {date_field}) = ?
            GROUP BY {sap_name_col}
        """
        params = (year, month)
    else:
        query = f"""
            SELECT {sap_name_col} as sap_name, SUM(quantity) as total_qty
            FROM {source_table}
            WHERE strftime('%Y', {date_field}) = ?
            GROUP BY {sap_name_col}
        """
        params = (year,)

    df = pd.read_sql_query(query, conn, params=params)

    # Truy xuất thông tin bổ sung từ bảng danh mục
    catalog_df = pd.read_sql_query(
        f"SELECT {sap_name_col}, {name_col}, sap_code, unit FROM {name_table}", conn)

    merged = pd.merge(catalog_df, df, how="left", left_on=sap_name_col, right_on="sap_name").fillna(0)

    label = "Tổng nhập" if action_type == "import" else "Tổng xuất"
    merged = merged.rename(columns={
        name_col: "Tên",
        sap_name_col: "Tên SAP",
        "sap_code": "Mã SAP",
        "unit": "Đơn vị",
        "total_qty": label
    })

    final_df = merged[["Tên", "Tên SAP", "Mã SAP", "Đơn vị", label]]
    conn.close()

    # Nếu người dùng yêu cầu export Excel
    if request.form.get("export_excel"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            final_df.to_excel(writer, sheet_name=f"{action_type}_{mode}_{year}", index=False)
        output.seek(0)
        return send_file(output, download_name=f"Thong_ke_{action_type}_{item_type}_{mode}_{year}.xlsx", as_attachment=True)

    return render_template("statistic_summary.html",
                           df=final_df,
                           item_type=item_type,
                           action_type=action_type,
                           year=year,
                           month=month,
                           mode=mode,
                           label=label)
