import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "7316266993:AAEh-D35CS-p8DIshB-IzZ-dJk_W80naZik"

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
        reply_markup=reply_markup
    )

# ---------------- BUTTON HANDLER ----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "download":
        await query.edit_message_text("📩 Send Instagram reel link to download")
    elif query.data == "help":
        await query.edit_message_text("ℹ️ Just send reel link, I will download it")

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
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("users", users))

print("Bot Running...")
app.run_polling()