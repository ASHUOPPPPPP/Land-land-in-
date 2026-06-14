import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7316266993:AAEh-D35CS-p8DIshB-IzZ-dJk_W80naZik"

def download_video(url):
    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "best",
        "noplaylist": True,
        "quiet": True,
        "retries": 5
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com" not in url:
        await update.message.reply_text("Only Instagram link bhejo.")
        return

    try:
        file_path = download_video(url)

        await update.message.reply_video(video=open(file_path, "rb"))
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"Failed:\n{e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("Bot Running...")
app.run_polling()