from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__, template_folder="templates")

@dashboard_bp.route("/dashboard")
def index():
    return render_template("dashboard.html")

@dashboard_bp.route("/import_menu")
def import_menu():
    return render_template("import_menu.html")

@dashboard_bp.route("/export_menu")
def export_menu():
    return render_template("export_menu.html")

@dashboard_bp.route("/statistic_menu")
def statistic_menu():
    return render_template("statistic_menu.html")
