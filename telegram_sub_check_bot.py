import requests
from flask import Flask, request
import time

app = Flask(__name__)

# Настройки
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHANNEL_ID = "@your_channel"
NIGHTBOT_WEBHOOK = "your_nightbot_webhook_url"
CHECK_TIMEOUT = 45  # Время ожидания логина (сек)

def check_subscription(user_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember"
    params = {"chat_id": TELEGRAM_CHANNEL_ID, "user_id": user_id}
    response = requests.get(url, params=params).json()
    
    if response.get("ok"):
        status = response["result"].get("status")
        return status in ["member", "administrator", "creator"]
    return False

def send_to_nightbot(message):
    requests.get(NIGHTBOT_WEBHOOK, params={"message": message})

@app.route('/check_subscription', methods=['POST'])
def check_subscription_api():
    data = request.json
    user_id = data.get("user_id")
    
    if not user_id:
        return {"status": "error", "message": "Telegram ID не предоставлен!"}, 400
    
    if check_subscription(user_id):
        message = "✅ Победитель подписан на канал!"
    else:
        message = "❌ Победитель НЕ подписан на канал!"
    
    send_to_nightbot(message)
    return {"status": "success", "message": message}

@app.route('/')
def home():
    return "Бот работает!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
