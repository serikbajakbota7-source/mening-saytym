from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "super_secret_key"

# Render-дегі базаға қосылу сілтемесі
DATABASE_URL = "postgresql://mening_db_user:RzX3a8IKl6f1JYYtLCT64tz6WAfYBqpW@dpg-d6qr4epj16oc73espbc0-a.oregon-postgres.render.com/mening_db"

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

# КЕСТЕНІ АВТОМАТТЫ ТҮРДЕ ҚҰРУ
def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                ip_address TEXT,
                reg_time TEXT,
                role TEXT DEFAULT 'user'
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("База сәтті тексерілді!")
    except Exception as e:
        print(f"База дайындауда қате: {e}")

init_db()

# --- МАРШРУТТАР ---

@app.route('/')
def registration_page():
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return redirect(url_for('home'))
        else:
            return "Қате: Логин немесе пароль дұрыс емес!" 
    except Exception as e:
        return f"Кіру кезінде қате: {e}"

@app.route('/home')
def home():
    return render_template('index.html')

# --- ЖАҢА: САБАҚТАР БЕТІНЕ АПАРАТЫН ЖОЛ ---
@app.route('/lesson')
def lesson():
    # Бұл маршрут lesson.html файлын ашады
    # URL-дегі ?lang=Python параметрін JavaScript өзі оқып алады
    return render_template('lesson.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    ip_addr = request.remote_addr
    reg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password, ip_address, reg_time) VALUES (%s, %s, %s, %s)',
                       (username, password, ip_addr, reg_time))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Тіркелу қатесі: {e}"

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
        return f"Админ панель қатесі: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
