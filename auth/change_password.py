from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import sqlite3

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "db", "my_data.db")


change_pw_bp = Blueprint('change_pw', __name__, template_folder='templates')

@change_pw_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        flash("Bạn chưa đăng nhập.", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    if request.method == 'POST':
        current_pw = request.form['current_password']
        new_pw = request.form['new_password']
        confirm_pw = request.form['confirm_password']

        # Kiểm tra nhập lại mật khẩu
        if new_pw != confirm_pw:
            flash("Mật khẩu mới không khớp!", "error")
            return redirect(url_for('change_pw.change_password'))

        # Kết nối DB và kiểm tra mật khẩu hiện tại
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM Users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            flash("User không tồn tại!", "error")
            return redirect(url_for('auth.login'))

        current_password_db = row[0]

        # So sánh mật khẩu hiện tại với mật khẩu nhập vào
        if current_pw != current_password_db:
            conn.close()
            flash("Mật khẩu hiện tại không đúng!", "error")
            return redirect(url_for('change_pw.change_password'))

        # Cập nhật mật khẩu mới
        cursor.execute("UPDATE Users SET password = ? WHERE user_id = ?", (new_pw, user_id))
        conn.commit()
        conn.close()

        flash("✅ Đổi mật khẩu thành công!", "success")
        return redirect(url_for('dashboard.index'))

    return render_template("change_password.html")
