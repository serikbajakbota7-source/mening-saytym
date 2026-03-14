from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# Сенің базаңның сілтемесі
DATABASE_URL = "postgresql://mening_db_user:RzX3a8IKl6f1JYYtLCT64tz6WAfYBqpW@dpg-d6qr4epj16oc73espbc0-a.oregon-postgres.render.com/mening_db"

def get_db_connection():
    # connect_timeout қостық, сайт босқа айналып тұрмауы үшін
    conn = psycopg2.connect(DATABASE_URL, sslmode='require', connect_timeout=5)
    return conn

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                ip_address VARCHAR(50),
                reg_time VARCHAR(50),
                role VARCHAR(20) DEFAULT 'user'
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

init_db()

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
        cursor.execute('INSERT INTO users (username, password, ip_address, reg_time) VALUES (%s, %s, %s, %s)',
                       (username, password, ip_addr, reg_time))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('home'))
    except Exception as e:
        return f"Қате: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Базадан осындай логин мен паролі бар адамды іздейміз
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        
        cursor.close()
        conn.close()

        if user:
            # Егер табылып тұрса, басты бетке жібереміз
            return redirect(url_for('home'))
        else:
            # Егер табылмаса, қате айтамыз
            return "Логин немесе пароль қате!"
    except Exception as e:
        return f"Кіру кезінде қате шықты: {e}"
