from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import os

app = Flask(__name__)

DB_FILE = 'military_logistics.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # 1. Tabel Publik: Data Logistik Militer (Banyak Data agar Shuffling Terlihat Jelas)
    cursor.execute("DROP TABLE IF EXISTS military_orders")
    cursor.execute("""
        CREATE TABLE military_orders (
            order_id TEXT,
            destination TEXT,
            cargo_type TEXT,
            quantity INTEGER,
            clearance_level TEXT
        )
    """)
    
    orders_data = [
        ('ORD-091', 'Sector-7 Outpost', 'Heavy Platoon Ammunition', 500, 'LEVEL-2'),
        ('ORD-104', 'Neo-Jakarta Port', 'Cybernetic Prosthetics', 120, 'LEVEL-1'),
        ('ORD-215', 'Sub-Orbital Station Alpha', 'Liquid Hydrogen Fuel Cells', 80, 'LEVEL-3'),
        ('ORD-312', 'Bunker 101 Deep Underground', 'Riot Control Exoskeletons', 45, 'LEVEL-2'),
        ('ORD-402', 'Antarctic Research Lab', 'Bio-Hazard Containment Units', 15, 'LEVEL-4'),
        ('ORD-551', 'Nuansa Desert Garrison', 'Automated Defense Turrets', 30, 'LEVEL-3'),
        ('ORD-609', 'Chiba Cyber-Grid Hub', 'Optical Fiber Quantum Relays', 250, 'LEVEL-1')
    ]
    cursor.executemany("INSERT INTO military_orders VALUES (?, ?, ?, ?, ?)", orders_data)
    
    # 2. Tabel Pengguna: Kredensial Akses
    cursor.execute("DROP TABLE IF EXISTS system_users")
    cursor.execute("CREATE TABLE system_users (username TEXT, access_role TEXT)")
    cursor.execute("INSERT INTO system_users VALUES ('operator_lyno', 'GUEST_MONITOR')")
    
    # 3. Tabel Rahasia: Lokasi Flag PicoCTF Style
    cursor.execute("DROP TABLE IF EXISTS flag_vault")
    cursor.execute("CREATE TABLE flag_vault (tracking_code TEXT, secret_flag TEXT)")
    cursor.execute("INSERT INTO flag_vault VALUES ('TRK-SECRET-2026', 'CTF{p1c0_0rd3r_by_bl1nd_full_sc4l3_r3pl1c4}')")
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    # Ambil parameter pencarian (search) dan pengurutan (order)
    search_query = request.args.get('search', '')
    sort_column = request.args.get('order', 'order_id')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # SKEMA LUAS & RENTAN:
    # Menggabungkan pencarian standar dengan kerentanan interpolasi string pada klausul ORDER BY
    # Injectable Point berada di variabel {sort_column}
    query = f"""
        SELECT order_id, destination, cargo_type, quantity, clearance_level 
        FROM military_orders 
        WHERE destination LIKE '%{search_query}%' OR cargo_type LIKE '%{search_query}%'
        ORDER BY {sort_column}
    """
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        error_message = None
    except Exception as e:
        rows = []
        # Mengembalikan error generik khas blind SQLi kompetisi profesional
        error_message = "SQL Execution Warning: Database syntax tracking encountered an anomaly."

    conn.close()
    return render_template('index.html', orders=rows, search=search_query, current_order=sort_column, error=error_message)

if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        init_db()
    app.run(host='0.0.0.0', port=5000)