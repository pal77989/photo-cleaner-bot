import telebot

# अपना Telegram Bot Token यहाँ डालो
BOT_TOKEN = "8036681804:AAEnhv-wM3KprJQl_T3a3NUZv1MccoRWBg"

# Bot को initialize करो
bot = telebot.TeleBot(BOT_TOKEN)

# Start command का handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! I am your Photo Cleaner Bot.\nSend me a photo and I’ll clean the background for you!")

# Photo receive करने का handler
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "📷 Got your photo! Processing... (Not implemented yet)")

# Bot को run करने के लिए
bot.polling()
