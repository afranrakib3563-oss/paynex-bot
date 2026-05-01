import telebot
from telebot import types
from flask import Flask
import threading
import os

# --- 1. BOT TOKEN ---
API_TOKEN = '8662954455:AAEdvRgMlyq4URewoN9O8rIqyOS08vnE0lk' 
bot = telebot.TeleBot(API_TOKEN)

# --- 2. SERVER FOR RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "PayNex Bot is Online!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()

# --- 3. BOT COMMANDS (ENGLISH) ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton('💰 Balance')
    item2 = types.KeyboardButton('📝 Tasks')
    item3 = types.KeyboardButton('💸 Withdraw')
    item4 = types.KeyboardButton('👥 Referral')
    markup.add(item1, item2, item3, item4)
    
    welcome_text = (f"Hello {message.from_user.first_name}!\n\n"
                    "Welcome to PayNex Official Bot.\n"
                    "Start earning USD by completing simple tasks.")
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == '💰 Balance':
        bot.reply_to(message, f"👤 User: {message.from_user.first_name}\n💵 Balance: $0.00 USD")
    elif message.text == '📝 Tasks':
        bot.reply_to(message, "⚠️ No tasks available at the moment.")
    elif message.text == '💸 Withdraw':
        bot.reply_to(message, "❌ Insufficient Balance!\n🔹 Minimum Withdraw: $0.25 USD")
    elif message.text == '👥 Referral':
        bot_info = bot.get_me()
        referral_link = f"https://t.me/{bot_info.username}?start={message.chat.id}"
        bot.reply_to(message, f"🔗 Your Referral Link:\n{referral_link}")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
