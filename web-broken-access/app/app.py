from flask import Flask, render_template, request, redirect, make_response, jsonify

app = Flask(__name__)

# Dummy Database internal kontainer
# ID 1 milik Admin (menyimpan Flag CTF)
# ID 2 milik Guest
DB_NOTES = {
    "1": {"owner": "admin", "content": "CTF{b0rk3n_4cc3ss_c0ntr0l_v1a_w1nd0ws}"},
    "2": {"owner": "guest", "content": "Halo guest! Ini catatan rahasia kamu. Tidak ada flag di sini."}
}

@app.route('/')
def index():
    user_id = request.cookies.get('user_id')
    role = request.cookies.get('role')
    
    if not user_id:
        resp = make_response(redirect('/'))
        resp.set_cookie('user_id', '2')
        resp.set_cookie('role', 'guest')
        return resp
        
    return render_template('index.html', role=role)

@app.route('/api/v1/notes')
def get_note():
    note_id = request.args.get('id')
    
    if not note_id:
        return jsonify({"error": "Missing parameter 'id'"}), 400
        
    if note_id in DB_NOTES:
        # CELAH KEAMANAN: Server tidak memvalidasi apakah user_id di cookie 
        # benar-benar berhak melihat note_id yang diminta.
        return jsonify(DB_NOTES[note_id])
    else:
        return jsonify({"error": "Note not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)