from flask import Flask, request, jsonify
from pymongo import MongoClient
import re
import requests
import json
from utils.loader import load_jurusan, load_jadwal, load_video_poster

app = Flask(__name__)

# MongoDB connection (optional, can be kept for hybrid use)
client = MongoClient("mongodb://localhost:27017")
db = client["chatbotppdb"]
# Akses ke masing-masing koleksi
data_jadwal_collection = db["data jadwal"]
data_jurusan_collection = db["datajurusan"]
data_poster_collection = db["dataposter"]

# Bot Token - Ganti dengan token bot Anda dari @BotFather
BOT_TOKEN = "7965405388:AAFYaYyXn92IwkFg93pNm01hcQNpiamV7lY"

# Load JSON-based data
jurusan_data = load_jurusan()
jadwal_data = load_jadwal()
video_data = load_video_poster()

def get_json_response(user_input):
    user_input = user_input.lower()

    if "profil" in user_input:
        return f"{video_data['data_video_profil']['judul']}\n {video_data['data_video_profil']['link']}"

    elif "poster" in user_input:
        return f"️ {video_data['data_poster']['deskripsi']}\n {video_data['data_poster']['link']}"

    elif "jadwal" in user_input:
        response = "\n".join([f"{item['tanggal']} - {item['kegiatan']}" for item in jadwal_data])
        return response

    elif "daya tampung" in user_input:
        jalur = "afirmasi" if "afirmasi" in user_input else "reguler"
        jurusan_found = None
        for item in jurusan_data:
            if item['jurusan'].lower() in user_input:
                jurusan_found = item
                break
        if jurusan_found:
            j = jurusan_found['jurusan']
            d = jurusan_found['jalur'][jalur]
            return (
                f"Jurusan: {j}\n"
                f"Jalur: {jalur.title()}\n"
                f"Daya Tampung: {d['daya_tampung']}\n"
                f"Nilai Terendah: {d['nilai_terendah']}\n"
                f"Nilai Tertinggi: {d['nilai_tertinggi']}\n"
                f"Rata-Rata: {d['rata_rata']}"
            )
        else:
            return "Jurusan tidak ditemukan. Contoh: daya tampung kuliner afirmasi"

    return None

def get_response(user_input):
    # Try JSON-based response first
    json_response = get_json_response(user_input)
    if json_response:
        return json_response

    # Fallback to rule-based (MongoDB)
    try:
        for rule in collection.find():
            if 'patterns' in rule and 'response' in rule:
                for pattern in rule['patterns']:
                    if re.search(r'\\b' + re.escape(pattern) + r'\\b', user_input, re.IGNORECASE):
                        response = rule['response']
                        return "\n".join(response) if isinstance(response, list) else response
        return "Perintah tidak dikenali. Coba ketik: jadwal, daya tampung kuliner afirmasi, profil, atau poster."
    except Exception as e:
        print(f"Error in get_response: {e}")
        return "Maaf, terjadi kesalahan sistem."

# def get_response(user_input):
#     # Try JSON-based response first
#     json_response = get_json_response(user_input)
#     if json_response:
#         return json_response

#     # Fallback to rule-based (MongoDB)
#     try:
#         for rule in collection.find():
#             if 'patterns' in rule and 'response' in rule:
#                 for pattern in rule['patterns']:
#                     if re.search(r'\\b' + re.escape(pattern) + r'\\b', user_input, re.IGNORECASE):
#                         response = rule['response']
#                         return "\n".join(response) if isinstance(response, list) else response
#         return "Maaf, saya belum mengerti pertanyaan Anda."
#     except Exception as e:
#         print(f"Error in get_response: {e}")
#         return "Maaf, terjadi kesalahan sistem."

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        if 'message' in update:
            message = update['message']
            chat_id = message['chat']['id']
            if 'text' in message:
                user_input = message['text'].strip()
                response_text = get_response(user_input)
                send_result = send_telegram_message(chat_id, response_text)
                return jsonify({"status": "success", "result": send_result})
        return jsonify({"status": "no_message"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Telegram Bot is running!",
        "webhook_endpoint": "/webhook",
        "bot_token": f"...{BOT_TOKEN[-10:]}"
    })

@app.route("/test", methods=["POST"])
def test():
    try:
        rules_count = collection.count_documents({})
        sample_rule = collection.find_one()
        return jsonify({
            "status": "Database connected",
            "rules_count": rules_count,
            "sample_rule": sample_rule
        })
    except Exception as e:
        return jsonify({
            "status": "Database error",
            "error": str(e)
        })

if __name__ == "__main__":
    print("Telegram Chatbot Flask server is running on http://localhost:5000")
    print("Webhook endpoint: /webhook")
    app.run(port=5000, debug=True)
