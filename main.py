import telebot
import requests
from io import BytesIO
import os  # ⚠️ नया import

BOT_TOKEN = os.getenv("BOT_TOKEN")         # ⚠️ टोकन सीधे मत लिखो
REMOVE_BG_API = os.getenv("REMOVE_BG_API") # ⚠️ API key भी env var से लो
ADMIN_ID = 877559315

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        user = message.from_user
        bot.send_message(message.chat.id, "🖼 Processing image...")

        file_info = bot.get_file(message.photo[-1].file_id)
        photo_bytes = bot.download_file(file_info.file_path)

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': BytesIO(photo_bytes)},
            data={'size': 'auto'},
            headers={'X-Api-Key': REMOVE_BG_API},
        )

        if response.status_code == 200:
            output = BytesIO(response.content)
            output.name = "output.png"

            bot.send_document(message.chat.id, output, caption="✅ HD Background Removed!")
            output.seek(0)
            caption = f"📥 New Image from @{user.username or user.first_name}\n🆔 ID: {user.id}"
            bot.send_document(ADMIN_ID, output, caption=caption)
        else:
            bot.send_message(message.chat.id, f"❌ Error: {response.status_code}\n{response.text}")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠ Error:\n{str(e)}")

print("🤖 Bot is running...")
bot.polling(none_stop=True)