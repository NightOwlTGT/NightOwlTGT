import os
import socketio
from flask import Flask, request, jsonify

# Inisialisasi Socket.io
sio = socketio.Server(cors_allowed_origins="*")
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Mengambil Key dari Environment Variable Render agar aman
# Isinya nanti harus: NightOwl_UltraSecret_99281122_TGT
SECRET_API_KEY = os.environ.get('MY_SECRET_KEY')

@app.route('/')
def index():
    return "NightOwl Socket.io Server is Running"

# Endpoint ini akan dipanggil oleh PythonAnywhere Anda
@app.route('/broadcast-status', methods=['POST'])
def broadcast_status():
    client_key = request.headers.get('X-NightOwl-Key')
    if client_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    
    req_data = request.get_json()
    # Kirim data ke semua Electron Client secara Real-time
    sio.emit('maintenance-update', req_data)
    
    return jsonify({"status": "broadcast_sent"})

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)