import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

TOKEN = "YOUR_TOKEN_HERE"

Q1, Q2, Q3 = range(3)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(
        [["Начать опрос"], ["О вакансии"]], resize_keyboard=True
    )
    await update.message.reply_text(
        "Привет, я чат-бот dr.glex! 👋\nГотов провести опрос кандидата.",
        reply_markup=keyboard,
    )

# Информация о вакансии
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Вакансия: помощник ортодонта\n"
        "• Аккуратность\n• Внимательность\n• Желание учиться",
    )

# Начало опроса
async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1️⃣ Как вас зовут?", reply_markup=ReplyKeyboardRemove()
    )
    return Q1

# Вопрос 1
async def q1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("2️⃣ Сколько вам лет?")
    return Q2

# Вопрос 2
async def q2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["age"] = update.message.text
    await update.message.reply_text("3️⃣ Есть ли опыт работы в стоматологии?")
    return Q3

# Вопрос 3
async def q3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["exp"] = update.message.text
    summary = (
        "Спасибо за ответы! 🤝\n\n"
        f"Имя: {context.user_data['name']}\n"
        f"Возраст: {context.user_data['age']}\n"
        f"Опыт: {context.user_data['exp']}"
    )
    await update.message.reply_text(summary)
    return ConversationHandler.END

# Фоллбэк для отмены
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Опрос отменён.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Начать опрос"), start_survey)],
        states={
            Q1: [MessageHandler(filters.TEXT & ~filters.COMMAND, q1)],
            Q2: [MessageHandler(filters.TEXT & ~filters.COMMAND, q2)],
            Q3: [MessageHandler(filters.TEXT & ~filters.COMMAND, q3)],
        },
        fallbacks=[MessageHandler(filters.Regex("Отмена"), cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("О вакансии"), info))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
