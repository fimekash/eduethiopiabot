import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

# --- CONFIG ---
BOT_TOKEN = "8399076842:AAEXifOrHsp_mt3E99khdD_A1EYlDcm9BCY"
ADMIN_CHAT_ID = 6872304983
MAIN_CHANNEL = "https://t.me/eduethiopia"
GRADE_9_LINK = "https://t.me/eduethiopia_Grade9"
GRADE_10_LINK = "https://t.me/eduethiopia_Grade10"
GRADE_11_LINK = "https://t.me/eduethiopia_Grade11"
GRADE_12_LINK = "https://t.me/eduethiopia_Grade12"
YOUTUBE_CHANNEL = "https://www.youtube.com/@eduethiopia"

# --- LOGGING ---
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# --- QUIZ QUESTIONS ---
QUIZ_QUESTIONS = [

    {
        "question": "🟩 What planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": 2
    },
    {
        "question": "🟥 ስለ ቁጥሮች፣ ተለዋዋጮች፣ ስሌቶችና ዝምድናቸው የሚያጠና የሒሳብ ዘርፍ ምን ይባላል?",
        "options": ["ጂኦሜትሪ", "አልጀብራ", "ካልኩለስ", "ቶፖሎጂ"],
        "answer": 2
    },
        {
        "question": "🟨 What is the chemical symbol for water?",
        "options": ["H2O", "O2", "CO2", "NaCl"],
        "answer": 0
    },
]

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🇪🇹🌟 **Welcome to Eduethiopia STEM Bot!** 🌟🇪🇹\n\n"
        "📚 Learn • Practice • Grow\n"
        "🟩 Grade 9 - 12 STEM Content\n"
        "🟨 Quizzes & Challenges\n"
        "🟥 Ask Questions Directly to Teacher\n\n"
        f"📢 Main Channel: {MAIN_CHANNEL}\n"
        f"📚 Grade 9: {GRADE_9_LINK}\n"
        f"📚 Grade 10: {GRADE_10_LINK}\n"
        f"📚 Grade 11: {GRADE_11_LINK}\n"
        f"📚 Grade 12: {GRADE_12_LINK}\n"
        f"🎥 YouTube: {YOUTUBE_CHANNEL}"
    )
    keyboard = [
        [InlineKeyboardButton("📚 Lessons", callback_data="lessons")],
        [InlineKeyboardButton("📝 Practice Quiz", callback_data="quiz")],
        [InlineKeyboardButton("💬 Ask a Question", callback_data="ask")],
        [InlineKeyboardButton("💖 Support Teacher", callback_data="support")]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

# --- LESSONS MENU ---
async def lessons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Grade 9 / 9ኛ ክፍል", url=GRADE_9_LINK)],
        [InlineKeyboardButton("Grade 10 / 10ኛ ክፍል", url=GRADE_10_LINK)],
        [InlineKeyboardButton("Grade 11 / 11ኛ ክፍል", url=GRADE_11_LINK)],
        [InlineKeyboardButton("Grade 12 / 12ኛ ክፍል", url=GRADE_12_LINK)],
        [InlineKeyboardButton("📺 YouTube", url=YOUTUBE_CHANNEL)]
    ]
    await query.edit_message_text("Choose your grade / ክፍልዎን ይምረጡ:", reply_markup=InlineKeyboardMarkup(keyboard))

# --- QUIZ ---
async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    question = QUIZ_QUESTIONS[0]
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"quiz_answer_0_{i}") for i, opt in enumerate(question["options"])]
    ]
    await query.edit_message_text(question["question"], reply_markup=InlineKeyboardMarkup(keyboard))

async def quiz_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, _, q_index, ans_index = query.data.split("_")
    q_index, ans_index = int(q_index), int(ans_index)
    correct = QUIZ_QUESTIONS[q_index]["answer"]
    if ans_index == correct:
        reply = "🟩 Correct! ጀግና!"
    else:
        reply = f"🟥 Wrong. Correct answer: {QUIZ_QUESTIONS[q_index]['options'][correct]}"
    await query.edit_message_text(reply)

# --- ASK ---
async def ask_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("💬 Please type your question now:")
    context.user_data["asking"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("asking"):
        question = update.message.text
        await context.bot.send_message(ADMIN_CHAT_ID, f"📩 New question from {update.effective_user.first_name}:\n{question}")
        await update.message.reply_text("✅ Your question has been sent to the teacher.")
        context.user_data["asking"] = False

# --- SUPPORT ---
async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "💖 **Support Edupia Teachers** 💖\n\n"
        "If you love our lessons, you can send a bonus:\n"
        "📱 Telebirr: 0915111564",
        "🏦 CBE ንግድ ባንክ : 1000204345205",
        "🏦 BOA አቢሲኒያ : 83725656",
        "🌍 PayPal: yourpaypal@example.com"
    )
    await query.edit_message_text(text, parse_mode="Markdown")

# --- MAIN ---
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(lessons_callback, pattern="^lessons$"))
app.add_handler(CallbackQueryHandler(quiz_callback, pattern="^quiz$"))
app.add_handler(CallbackQueryHandler(quiz_answer_callback, pattern="^quiz_answer_"))
app.add_handler(CallbackQueryHandler(ask_callback, pattern="^ask$"))
app.add_handler(CallbackQueryHandler(support_callback, pattern="^support$"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
