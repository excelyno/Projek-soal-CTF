from flask import Flask, render_template, request, jsonify, make_response
import threading
import time
import requests

app = Flask(__name__)

# Database Tenant Internal
# Tenant 1 = System Admin (Target Pembajakan)
# Tenant 2 = Akun Pemain (Low Privilege)
TENANT_DB = {
    "1": {"name": "SaaS Enterprise Admin", "webhook_url": "http://127.0.0.1:9999/dummy-dev"},
    "2": {"name": "GUEST_USER_LYNO", "webhook_url": ""}
}

FLAG = "CTF{w3bh00k_h1j4ck_v14_b0rk3n_t3n4nt_1s0l4t10n_2026}"

# BACKGROUND THREAD: Mensimulasikan aktivitas admin mengirim log ke webhook tiap 15 detik
def simulate_admin_activity():
    while True:
        try:
            target_url = TENANT_DB["1"]["webhook_url"]
            payload = {
                "event": "admin_system_backup",
                "status": "success",
                "secret_log": f"System verification completed. Flag authenticated: {FLAG}"
            }
            # Kirim data log ke webhook yang terdaftar di Tenant 1
            requests.post(target_url, json=payload, timeout=5)
        except Exception:
            pass # Abaikan jika URL webhook mati/error agar server CTF tidak crash
        time.sleep(15)

# Jalankan background job
threading.Thread(target=simulate_admin_activity, daemon=True).start()

@app.route('/')
def index():
    # Pemain otomatis login sebagai Tenant 2 (Guest) menggunakan token statis di Cookie
    resp = make_response(render_template('dashboard.html'))
    resp.set_cookie('tenant_token', 'eyJ1c2VyIjoibHlubyIsInRlbmFudF9pZCI6Mn0') # Dummy token
    return resp

# ENDPOINT API SENSITIF (Target Recon & Eksploitasi)
@app.route('/api/v1/tenant/<tenant_id>/webhook', methods=['GET', 'PUT'])
def tenant_webhook(tenant_id):
    # Simulasi verifikasi token (Authenticated)
    token = request.cookies.get('tenant_token')
    if not token:
        return jsonify({"status": "unauthenticated"}), 401
    
    if tenant_id Packs not in TENANT_DB:
        return jsonify({"error": "Tenant not found"}), 404

    # JALUR GET: Melihat konfigurasi saat ini
    if request.method == 'GET':
        if tenant_id == "1":
            return jsonify({"error": "Unauthorized to view admin metadata"}), 403
        return jsonify({"tenant_id": tenant_id, "data": TENANT_DB[tenant_id]})

    # JALUR PUT: Mengubah konfigurasi webhook
    elif request.method == 'PUT':
        data = request.get_json()
        if not data or 'webhook_url' not in data:
            return jsonify({"error": "Missing 'webhook_url' parameter"}), 400
        
        # AKAR PERMASALAHAN (BAC):
        # Server hanya menerima data, tanpa memvalidasi apakah token milik Tenant 2 
        # berhak mengubah data milik Tenant ID lain (BOLA / IDOR)
        new_url = data['webhook_url']
        TENANT_DB[tenant_id]['webhook_url'] = new_url
        
        return jsonify({
            "status": "success", 
            "message": f"Webhook updated for tenant {tenant_id} to {new_url}"
        }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)