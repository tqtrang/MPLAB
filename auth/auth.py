from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

auth_bp = Blueprint('auth', __name__)
DB_PATH = r"C:\Users\TRANG\my_app\db\my_data.db"
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT user_name, role, password FROM Users WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            user_name, role_str, stored_password = result

            if password == stored_password:  # Nếu sau này mã hóa thì đổi thành check hash
                session['user_id'] = user_id
                session['user_name'] = user_name
                session['roles'] = [r.strip() for r in role_str.split(',')] if role_str else []
                return redirect(url_for('dashboard.index'))
            else:
                flash("Mật khẩu không đúng!", "error")
        else:
            flash("User ID không tồn tại.", "error")

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



