from flask import Flask, redirect, url_for
from auth import auth_bp
from material import material_bp, view_bp, log_mat_bp, export_mat_bp
from chemical import chemical_bp, view_chem_bp,log_chem_bp, export_chem_bp
from inventory import inventory_bp
from dashboard import dashboard_bp
from export_view.view_export import view_export_bp
from auth.change_password import change_pw_bp

import os




app = Flask(__name__)
app.secret_key = "your-secret-key"  # Bắt buộc cho session
print("📦 DB path exists:", os.path.exists("db/my_data.db"))
print("📁 Working directory:", os.getcwd())

# Đăng ký các blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(material_bp)
app.register_blueprint(view_bp)
app.register_blueprint(chemical_bp)
app.register_blueprint(view_chem_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(log_chem_bp)
app.register_blueprint(log_mat_bp)
app.register_blueprint(export_mat_bp)
app.register_blueprint(export_chem_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(view_export_bp)
app.register_blueprint(change_pw_bp)

@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render tự cấp port qua biến môi trường
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.run(host="0.0.0.0", port=port, debug=True)
    

print(app.url_map)

from scripts import seed_admin
seed_admin.run()
