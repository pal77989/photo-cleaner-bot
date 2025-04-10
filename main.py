import telebot
import os
import requests

# Bot Token
BOT_TOKEN = "7621303746:AAFyJSGE422LYduFsuU4_VpAdeijneW-KIs"
bot = telebot.TeleBot(BOT_TOKEN)

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Welcome to *PhotoCleaner Bot*! Send me any photo and I will remove its background.", parse_mode='Markdown')

# Handle photo
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("input_image.png", 'wb') as new_file:
            new_file.write(downloaded_file)

        # Send to remove.bg API (your working remove.bg token or change with local later)
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open('input_image.png', 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'h3Hw6ncz9RwdSocet1Wbh95e'}
        )

        if response.status_code == requests.codes.ok:
            with open('no_bg.png', 'wb') as out:
                out.write(response.content)
            bot.send_photo(message.chat.id, open('no_bg.png', 'rb'), caption="✅ Background removed!")
        else:
            bot.reply_to(message, "❌ Error removing background. Try again later.")
            print("Remove.bg error:", response.text)

    except Exception as e:
        print("Error:", e)
        bot.reply_to(message, "⚠️ Something went wrong.")

# Polling
bot.infinity_polling()
