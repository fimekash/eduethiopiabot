import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# --- CONFIG ---
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Replace with your BotFather token
ADMIN_CHAT_ID = 123456789  # Replace with your Telegram user ID
GRADE_9_LINK = 't.me/eduethiopia_Grade9'
GRADE_10_LINK = 't.me/eduethiopia_Grade10'
MAIN_CHANNEL = 't.me/eduethiopia'
YOUTUBE_CHANNEL = 'https://www.youtube.com/@eduethiopia'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "እንኳን ወደ Edu_pia STEM Bot በደህና መጡ!\\nWelcome to Edu_pia STEM Bot!"
    keyboard = [[InlineKeyboardButton("📚 Lessons / ትምህርቶች", callback_data='lessons')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def lessons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Grade 9 / ክፍል 9", callback_data='grade9')],
        [InlineKeyboardButton("Grade 10 / ክፍል 10", callback_data='grade10')]
    ]
    await query.edit_message_text("Choose your grade / ክፍልዎን ይምረጡ:", reply_markup=InlineKeyboardMarkup(keyboard))

async def grade_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == 'grade9':
        text = f"📢 Main Channel: {MAIN_CHANNEL}\\n📚 Grade 9 Group: {GRADE_9_LINK}\\n🎥 YouTube: {YOUTUBE_CHANNEL}"
    else:
        text = f"📢 Main Channel: {MAIN_CHANNEL}\\n📚 Grade 10 Group: {GRADE_10_LINK}\\n🎥 YouTube: {YOUTUBE_CHANNEL}"
    keyboard = [[InlineKeyboardButton("📺 Watch Latest Lesson", url=YOUTUBE_CHANNEL)]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(lessons_callback, pattern='^lessons$'))
app.add_handler(CallbackQueryHandler(grade_selection, pattern='^grade9$|^grade10$'))

print("Bot is running...")
app.run_polling()
