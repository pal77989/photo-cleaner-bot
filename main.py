from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from rembg import remove
from dotenv import load_dotenv

# Load token from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send me a photo and I will remove its background.")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    input_path = "input.png"
    output_path = "output.png"
    await file.download_to_drive(input_path)

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            o.write(remove(i.read()))

    await update.message.reply_photo(photo=open(output_path, 'rb'))

    os.remove(input_path)
    os.remove(output_path)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()