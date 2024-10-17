from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime

app = Flask(__name__)

# Fungsi untuk membaca data dari file .json
def read_data_from_json():
    if not os.path.exists('data.json'):
        return {}
    
    with open('data.json', 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

# Fungsi untuk menulis data ke file .json
def write_data_to_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Route untuk menyajikan halaman HTML
@app.route('/')
def index():
    return render_template('index.html')

# API untuk menambahkan data username, tanggal expired, dan tipe pengguna
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data or 'username' not in data or 'expired_date' not in data or 'user_type' not in data:
        return jsonify({"error": "Username, expired_date, and user_type are required"}), 400

    username = data['username']
    expired_date = data['expired_date']
    user_type = data['user_type']

    # Validasi tipe pengguna
    if user_type not in ['free', 'premium']:
        return jsonify({"error": "User type must be 'free' or 'premium'"}), 400

    # Membaca data dari file .json
    current_data = read_data_from_json()

    # Cek apakah username sudah ada
    if username in current_data:
        return jsonify({"error": "Username already exists"}), 400

    # Menambahkan data baru
    current_data[username] = {
        "expired_date": expired_date,
        "user_type": user_type
    }

    # Menyimpan data ke file .json
    write_data_to_json(current_data)

    return jsonify({"message": "User added successfully", "data": current_data[username]}), 200

# API untuk mengecek apakah username sudah ada dan apakah expired
@app.route('/check_user/<username>', methods=['GET'])
def check_user(username):
    # Membaca data dari file .json
    current_data = read_data_from_json()

    # Cek apakah username ada di data
    if username not in current_data:
        return jsonify({"error": "Username not found"}), 404

    # Mendapatkan tanggal expired dan tipe pengguna
    expired_date_str = current_data[username]['expired_date']
    user_type = current_data[username]['user_type']
    expired_date = datetime.strptime(expired_date_str, "%Y-%m-%d").date()
    
    # Memeriksa apakah username sudah expired
    today = datetime.today().date()
    
    if today > expired_date:
        return jsonify({"message": "Username is expired", "expired_date": expired_date_str, "user_type": user_type}), 200
    else:
        return jsonify({"message": "Username found and active", "data": current_data[username]}), 200

if __name__ == '__main__':
    app.run(debug=True)
