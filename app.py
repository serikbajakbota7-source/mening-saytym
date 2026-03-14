from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime
import os

app = Flask(__name__)

# Render-дегі базаға қосылу сілтемесі
# Егер базаң өшіп қалса, осы жердегі сілтемені жаңарту керек
DATABASE_URL = "postgresql://mening_db_user:RzX3a8IKl6f1JYYtLCT64tz6WAfYBqpW@dpg-d6qr4epj16oc73espbc0-a.oregon-postgres.render.com/mening_db"

def get_db_connection():
    # sslmode='require' Render базасы үшін міндетті
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
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
    # Render үшін портты автоматты түрде алу маңызды
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
