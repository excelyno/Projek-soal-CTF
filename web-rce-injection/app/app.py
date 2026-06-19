from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ""
    if request.method == 'POST':
        target_ip = request.form.get('ip')
        
        if target_ip:
            # AKAR MASALAH (Command Injection):
            # Input dari user langsung digabungkan ke string perintah sistem tanpa filter!
            # Jika user memasukkan "127.0.0.1; ls", sistem akan menjalankan: ping -c 1 127.0.0.1; ls
            command = f"ping -c 1 {target_ip}"
            
            try:
                # Eksekusi ke terminal Linux internal kontainer
                result = os.popen(command).read()
            except Exception as e:
                result = str(e)
                
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)