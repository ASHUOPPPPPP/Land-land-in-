import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN"

# ---------------- USER SAVE SYSTEM ----------------
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
        "👋 Welcome to ASHU Bot!\nChoose option below:",
        reply_markup