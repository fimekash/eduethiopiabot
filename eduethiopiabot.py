import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from telegram.helpers import escape_markdown

# --- CONFIG ---
BOT_TOKEN = "8399076842:AAFQ3M5gj4TmD9ZaeyIfqP9lWcxJPYl6fVo"
ADMIN_CHAT_ID = 6872304983

MAIN_CHANNEL = "https://t.me/eduethiopia"
GRADE_9_LINK = "https://t.me/eduethiopia_Grade9"
GRADE_10_LINK = "https://t.me/eduethiopia_Grade10"
GRADE_11_LINK = "https://t.me/eduethiopia_Grade11"
GRADE_12_LINK = "https://t.me/eduethiopia_Grade12"
YOUTUBE_CHANNEL = "https://www.youtube.com/@eduethiopia"

# --- LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- QUIZ QUESTIONS ---
QUIZ_QUESTIONS = [
    {
        "question": "🟨 What is the chemical symbol for water?",
        "options": ["H₂O", "O₂", "CO₂", "NaCl"],
        "answer": 0
    },
    {
        "question": "🟩 What planet is known as the Red Planet?",
        "options": ["Earth", "Venus", "Mars", "Jupiter"],
        "answer": 2
    },
    {
        "question": "🟥 በሂሳብ ውስጥ፣ ሶስት ማእዘን ያለው አካል ምንድነው?",
        "options": ["ቀመር", "ማእዘን", "ሶስት ማእዘን", "ኩብ"],
        "answer": 2
    }
]

# --- START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🇪🇹🌟 *Welcome to Eduethiopia STEM Bot!* 🌟🇪🇹\n\n"
        "📚 Learn • Practice • Grow\n"
        "🟩 Grade 9 - 12 STEM Content\n"
        "🟨 Quizzes & Challenges\n"
        "🟥 Ask Questions Directly to Teacher\n\n"
        f"[📢 Main Channel]({MAIN_CHANNEL})\n"
        f"[📚 Grade 9]({GRADE_9_LINK})\n"
        f"[📚 Grade 10]({GRADE_10_LINK})\n"
        f"[📚 Grade 11]({GRADE_11_LINK})\n"
        f"[📚 Grade 12]({GRADE_12_LINK})\n"
        f"[🎥 YouTube]({YOUTUBE_CHANNEL})"
    )

    keyboard = [
        [InlineKeyboardButton("📚 Lessons", callback_data="lessons")],
        [InlineKeyboardButton("📝 Practice Quiz", callback_data="quiz_start")],
        [InlineKeyboardButton("💬 Ask a Question", callback_data="ask")],
        [InlineKeyboardButton("💖 Support Teacher", callback_data="support")]
    ]

    await update.message.reply_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="MarkdownV2"
    )

# --- LESSONS MENU ---
async def lessons_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Grade 9 / 9ኛ ክፍል", url=GRADE_9_LINK)],
        [InlineKeyboardButton("Grade 10 / 10ኛ ክፍል", url=GRADE_10_LINK)],
        [InlineKeyboardButton("Grade 11 / 11ኛ ክፍል", url=GRADE_11_LINK)],
        [InlineKeyboardButton("Grade 12 / 12ኛ ክፍል", url=GRADE_12_LINK)],
        [InlineKeyboardButton("📺 YouTube", url=YOUTUBE_CHANNEL)],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="start_menu")]
    ]
    await query.edit_message_text(
        "Choose your grade / ክፍልዎን ይምረጡ:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- QUIZ START ---
async def quiz_start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["quiz_index"] = 0
    context.user_data["quiz_score"] = 0
    await send_quiz_question(query, context)

async def send_quiz_question(query, context):
    q_index = context.user_data["quiz_index"]
    if q_index >= len(QUIZ_QUESTIONS):
        score = context.user_data["quiz_score"]
        await query.edit_message_text(f"🏆 Quiz completed! Your score: {score}/{len(QUIZ_QUESTIONS)}")
        return

    question = QUIZ_QUESTIONS[q_index]
    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"quiz_answer_{q_index}_{i}")]
        for i, opt in enumerate(question["options"])
    ]
    await query.edit_message_text(question["question"], reply_markup=InlineKeyboardMarkup(keyboard))

async def quiz_answer_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    if len(parts) != 4:
        return

    _, _, q_index, ans_index = parts
    q_index, ans_index = int(q_index), int(ans_index)
    correct = QUIZ_QUESTIONS[q_index]["answer"]

    if ans_index == correct:
        reply = "🟩 Correct! Great job!"
        context.user_data["quiz_score"] += 1
    else:
        reply = f"🟥 Wrong. Correct answer: {QUIZ_QUESTIONS[q_index]['options'][correct]}"

    await query.message.reply_text(reply)
    context.user_data["quiz_index"] += 1
    await send_quiz_question(query, context)

# --- ASK A QUESTION ---
async def ask_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("💬 Please type your question now:")
    context.user_data["asking"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("asking"):
        if not update.message.text:
            await update.message.reply_text("❌ Please send text only.")
            return

        question = update.message.text
        name = escape_markdown(update.effective_user.first_name, version=2)
        question_text = escape_markdown(question, version=2)

        await context.bot.send_message(
            ADMIN_CHAT_ID,
            f"📩 New question from {name}:\n{question_text}",
            parse_mode="MarkdownV2"
        )
        await update.message.reply_text("✅ Your question has been sent to the teacher.")
        context.user_data["asking"] = False

# --- SUPPORT ---
async def support_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    text = (
        "💖 *Support Eduethiopia Teacher* 💖\n\n"
        "If you love our lessons, you can send a bonus:\n"
        "📱 Telebirr: 0915111564\n"
        "🏦 BOA አቢሲኒያ: 83725656\n"
        "🏦 CBE ንግድ ባንክ: 1000204345205\n"
        "🌍 PayPal: yourpaypal@example.com"
    )
    await query.edit_message_text(text, parse_mode="MarkdownV2")

# --- BACK TO MENU ---
async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

# --- ERROR HANDLER ---
async def error_handler(update, context):
    logging.error(msg="Exception while handling an update:", exc_info=context.error)

# --- MAIN ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))

    # CallbackHandlers
    app.add_handler(CallbackQueryHandler(lessons_callback, pattern="^lessons$"))
    app.add_handler(CallbackQueryHandler(quiz_start_callback, pattern="^quiz_start$"))
    app.add_handler(CallbackQueryHandler(quiz_answer_callback, pattern="^quiz_answer_"))
    app.add_handler(CallbackQueryHandler(ask_callback, pattern="^ask$"))
    app.add_handler(CallbackQueryHandler(support_callback, pattern="^support$"))
    app.add_handler(CallbackQueryHandler(start_callback, pattern="^start_menu$"))

    # Message Handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error_handler)

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()