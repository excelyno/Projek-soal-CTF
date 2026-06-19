from flask import Flask, render_template, request, redirect, make_response, send_from_directory
import hashlib
import os

app = Flask(__name__)

# Password asli: adminp4ss
ADMIN_HASH = "93d8b51239aa806b7daaf688321cb170"
FLAG = "CTF{md5_w1th0ut_s4lt_1s_us3l3ss_2026}"

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Menggunakan MD5 tanpa salt (Cryptographic Failure)
        hashed_input = hashlib.md5(password.encode()).hexdigest()
        
        if username == 'admin' and hashed_input == ADMIN_HASH:
            resp = make_response(redirect('/admin-dashboard'))
            resp.set_cookie('session_secret', 'admin_logged_in_token_xyz')
            return resp
        else:
            error = "Username atau Password salah, wok!"
            
    return render_template('index.html', error=error)

@app.route('/admin-dashboard')
def admin():
    session = request.cookies.get('session_secret')
    if session == 'admin_logged_in_token_xyz':
        return render_template('admin.html', flag=FLAG)
    return redirect('/')

# Endpoint robot pencari (Petunjuk CTF)
@app.route('/robots.txt')
def robots():
    return "User-agent: *\nDisallow: /secret-backup-db-xyz.sql"

# Endpoint file backup yang bocor
@app.route('/secret-backup-db-xyz.sql')
def backup():
    content = """
    -- CTF Database Backup Dump
    -- Table structure for table `users`
    --
    CREATE TABLE `users` (
      `username` varchar(50),
      `password_md5` varchar(32)
    );
    
    INSERT INTO `users` VALUES ('admin', 'd86863a4d839d195805e39363613b6fe');
    """
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)