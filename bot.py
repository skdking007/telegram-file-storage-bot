from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 10000))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        file_id = context.args[0]
        await update.message.reply_document(file_id)
    else:
        await update.message.reply_text(
            "👋 File Storage Bot\n\n"
            "Send me:\n🎥 Videos\n📦 APK / Apps\n\n"
            "I'll give you a download link 🔗"
        )

async def save_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    file = msg.document or msg.video
    file_id = file.file_id
    file_name = getattr(file, "file_name", "video.mp4")

    bot_username = (await context.bot.get_me()).username
    link = f"https://t.me/{bot_username}?start={file_id}"

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("⬇️ Download File", url=link)]]
    )

    await msg.reply_text(
        f"✅ File Saved\n📁 {file_name}\n🔗 Download:",
        reply_markup=keyboard
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.Video.ALL, save_file))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=os.environ.get("RENDER_EXTERNAL_URL")
    )

if __name__ == "__main__":
    main()
