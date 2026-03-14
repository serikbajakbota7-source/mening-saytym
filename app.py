from flask import Flask, render_template, request, redirect, url_for
import psycopg2  # Sqlite3-тің орнына осыны қолданамыз
from datetime import datetime

app = Flask(__name__)

# Бұл жерде базаға қосылу мәліметтерін жазамыз
# Пароль деген жерге pgAdmin-ге кіретін пароліңді жаз
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="mening_bazam",
        user="postgres",
        password="СЕНІҢ_ПАРОЛІҢ"  # ОСЫ ЖЕРГЕ ПАРОЛЬ ЖАЗ!
    )
    return conn

@app.route('/')
def registration():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_addr = request.remote_addr
    reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # PostgreSQL-де сұрақ белгісінің (?) орнына %s қолданылады
        cursor.execute('INSERT INTO users (username, password, ip_address, reg_time) VALUES (%s, %s, %s, %s)',
                       (username, password, ip_addr, reg_time))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Қате орын алды: {e}"

@app.route('/admin')
def admin_panel():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, ip_address, reg_time, role FROM users')
        all_users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('admin.html', users=all_users)
    except Exception as e:
        return f"Базаға қосылу мүмкін болмады: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)