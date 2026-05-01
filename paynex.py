import telebot
from telebot import types
import os
from flask import Flask
from threading import Thread

# Configuration
API_TOKEN = '8662954455:AAEdvRgMlyq4URewoN9O8rIqyOS08vnE0lk'
ADMIN_ID = 8620155936

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

# Temporary Database
users = {}

@app.route('/')
def home():
    return "PayNex Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

# User Menu Keyboard
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('💰 Balance'),
        types.KeyboardButton('📝 Tasks'),
        types.KeyboardButton('👥 Referral'),
        types.KeyboardButton('💸 Withdraw')
    )
    return markup

# Admin Menu Keyboard
def admin_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        types.KeyboardButton('📊 Total Users'),
        types.KeyboardButton('📢 Broadcast'),
        types.KeyboardButton('🔙 Back to User Menu')
    )
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = {'balance': 0, 'referrals': 0}
    
    bot.send_message(
        message.chat.id, 
        f"Welcome {message.from_user.first_name} to PayNex Official Bot! 🚀\nStart earning by completing simple tasks.",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🛠 Welcome Admin! Control your bot here:", reply_markup=admin_menu())
    else:
        bot.send_message(message.chat.id, "❌ Access Denied! Unauthorized user.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    
    # User Menu Options
    if message.text == '💰 Balance':
        balance = users.get(user_id, {}).get('balance', 0)
        bot.send_message(message.chat.id, f"👤 User: {message.from_user.first_name}\n💰 Your Balance: {balance} BDT")
        
    elif message.text == '👥 Referral':
        bot.send_message(message.chat.id, f"🔗 Your Referral Link:\nhttps://t.me/{(bot.get_me()).username}?start={user_id}")
        
    elif message.text == '📝 Tasks':
        bot.send_message(message.chat.id, "🚫 No tasks available right now. Stay tuned!")
        
    elif message.text == '💸 Withdraw':
        bot.send_message(message.chat.id, "⚠️ Minimum withdraw limit: 50 BDT.")

    # Admin Menu Options
    elif message.text == '📊 Total Users' and user_id == ADMIN_ID:
        bot.send_message(message.chat.id, f"📈 Total Registered Users: {len(users)}")
        
    elif message.text == '📢 Broadcast' and user_id == ADMIN_ID:
        msg = bot.send_message(message.chat.id, "Enter the message you want to broadcast to all users:")
        bot.register_next_step_handler(msg, send_broadcast)

    elif message.text == '🔙 Back to User Menu':
        bot.send_message(message.chat.id, "Switching to User Interface...", reply_markup=main_menu())

def send_broadcast(message):
    count = 0
    for user in users:
        try:
            bot.send_message(user, f"📢 **NOTICE**\n\n{message.text}", parse_mode="Markdown")
            count += 1
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ Broadcast sent to {count} users.")

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    bot.infinity_polling()
    
