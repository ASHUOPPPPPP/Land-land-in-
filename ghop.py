import json
import os
import yt_dlp
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8682657556:AAEkrUX_geaUmhRHwnVc5BcY1TGdDo3jOOc"

progress_msg = None

# ---------------- USERS SAVE ----------------
def save_user(user):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except:
        users = []

    if user not in users:
        users.append(user)

    with open("users.json", "w") as f:
        json.dump(users, f)

# ---------------- PROGRESS BAR ----------------
def bar(percent):
    total = 10
    filled = int(percent / 10)
    empty = total - filled
    return "█" * filled + "░" * empty

async def loading_animation():
    global progress_msg
    for i in range(0, 101, 10):
        try:
            await progress_msg.edit_text(f"📥 Downloading...\n[{bar(i)}] {i}%")
            await asyncio.sleep(0.4)
        except:
            break

# ---------------- DOWNLOAD FUNCTION ----------------
def download_reel(url):
    ydl_opts = {
        "outtmpl": "video.%(ext)s",
        "format": "best",
        "noplaylist": True,
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ---------------- /START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.username or update.effective_user.first_name
    save_user(user)

    keyboard = [
        [InlineKeyboardButton("⬇️ Download Reel", callback_data="download")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")],
        [InlineKeyboardButton("👤 Developer @ASHU_XOP", url="https://t.me/ASHU_XOP")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome to ASHU Bot!\nSend Instagram reel link or use buttons below:",
        reply_markup=reply_markup
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "download":
        await query.edit_message_text("📩 Ab Instagram reel link bhejo")
    elif query.data == "help":
        await query.edit_message_text("ℹ️ Sirf Instagram reel link bhejo")

# ---------------- MESSAGE HANDLER ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global progress_msg

    url = update.message.text

    if "instagram.com" not in url:
        return

    progress_msg = await update.message.reply_text("📥 Starting download...\n[░░░░░░░░░░] 0%")

    task = asyncio.create_task(loading_animation())

    try:
        file_path = await asyncio.to_thread(download_reel, url)

        await progress_msg.edit_text("⬆️ Uploading video...")

        video = open(file_path, "rb")

        await update.message.reply_video(
            video=video,
            caption="✅ Download completed!\n🤖 ASHU Bot"
        )

        video.close()
        os.remove(file_path)

    except Exception as e:
        await progress_msg.edit_text(f"❌ Error:\n{e}")

# ---------------- /USERS ----------------
async def users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("users.json", "r") as f:
            users = json.load(f)

        text = "👥 Bot Users:\n\n" + "\n".join(users)

        await update.message.reply_text(text)

    except:
        await update.message.reply_text("No users found yet")

# ---------------- APP ----------------
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("users", users))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")
app.run_polling()