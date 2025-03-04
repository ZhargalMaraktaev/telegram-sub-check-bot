import requests
import time

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

def main():
    print("Ожидание логина победителя...")
    start_time = time.time()
    user_id = None  # Здесь должен быть Telegram ID, полученный от победителя
    
    while time.time() - start_time < CHECK_TIMEOUT:
        user_id = input("Введите Telegram ID победителя: ")
        if user_id:
            break
    
    if not user_id:
        print("Время вышло! Победитель не предоставил логин.")
        send_to_nightbot("Победитель не предоставил логин вовремя!")
        return
    
    if check_subscription(user_id):
        message = "✅ Победитель подписан на канал!"
    else:
        message = "❌ Победитель НЕ подписан на канал!"
    
    print(message)
    send_to_nightbot(message)

if __name__ == "__main__":
    main()
