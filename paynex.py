import telebot

api = "8662954455:AAEdvRgMlyq4URewoN9O8rIqyOS08vnE0lk"
bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    full_text = (
        "👋 Welcome!\n\n"
        "ℹ️ This bot helps you earn money by doing simple tasks.\n\n"
        "By using this Bot, you automatically agree to the current Terms of Use and Privacy Policy.👉\n"
        "https://telegra.ph/Terms-of-Use-06-07-2"
    )
    bot.send_message(message.chat.id, full_text, disable_web_page_preview=False)

if __name__ == "__main__":
    bot.polling(none_stop=True)
  
