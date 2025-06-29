import requests
import time
import os
from keep_alive import keep_alive

# Jalankan server keep-alive
keep_alive()

TOKEN = "8113974411:AAFXXFVep-aWHhpa3PLu-Cv3sOxmaUc2tE0"
CHAT_ID = "-1001872084141"
ADMIN_IDS = [7274015019]
INTERVAL = 300
PESAN_FILE = "pesan.txt"
LAST_UPDATE_FILE = "last_update.txt"

def load_pesan():
    if not os.path.exists(PESAN_FILE):
        return "⏰ Ini pesan otomatis default."
    with open(PESAN_FILE, "r", encoding="utf-8") as f:
        return f.read()

def simpan_pesan(pesan):
    with open(PESAN_FILE, "w", encoding="utf-8") as f:
        f.write(pesan)

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❌ Error kirim:", str(e))

def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    try:
        response = requests.get(url).json()
        return response["result"]
    except:
        return []

def handle_commands(updates):
    for update in updates:
        if "message" not in update:
            continue
        message = update["message"]
        user_id = message["from"]["id"]
        text = message.get("text", "")
        update_id = update["update_id"]

        if text.startswith("/setpesan") and user_id in ADMIN_IDS:
            bagian = text.split(" ", 1)
            if len(bagian) == 2:
                simpan_pesan(bagian[1])
                balas("✅ Pesan diupdate.", message["chat"]["id"])
            else:
                balas("⚠️ Format: /setpesan <pesan>", message["chat"]["id"])

        with open(LAST_UPDATE_FILE, "w") as f:
            f.write(str(update_id + 1))

def balas(text, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def get_last_update_id():
    if not os.path.exists(LAST_UPDATE_FILE):
        return None
    with open(LAST_UPDATE_FILE, "r") as f:
        return int(f.read())

print("🤖 Bot aktif...")
timer = 0
keep_alive()
while True:
    offset = get_last_update_id()
    updates = get_updates(offset)
    handle_commands(updates)

    if timer <= 0:
        send_message(load_pesan())
        timer = INTERVAL
    else:
        timer -= 5

    time.sleep(5)
