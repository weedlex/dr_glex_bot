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

# -----------------------
# Переменные окружения
# -----------------------
TOKEN = os.environ.get("BOT_TOKEN")  # Добавьте BOT_TOKEN на Render
ADMIN_CHAT_ID = int(os.environ.get("ADMIN_CHAT_ID"))  # Добавьте ADMIN_CHAT_ID на Render

# Проверка
if not TOKEN or not ADMIN_CHAT_ID:
    raise ValueError("Необходимо установить переменные окружения BOT_TOKEN и ADMIN_CHAT_ID")

# -----------------------
# Константы опроса
# -----------------------
(Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17) = range(17)

survey_keyboard = ReplyKeyboardMarkup([["Отмена"]], resize_keyboard=True)

# -----------------------
# Команды бота
# -----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup([["Начать опрос"], ["О вакансии"]], resize_keyboard=True)
    await update.message.reply_text(
        "Привет! Я чат-бот dr.glex 👋\nГотов провести опрос кандидата.",
        reply_markup=keyboard
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Вакансия: помощник ортодонта\n• Аккуратность\n• Внимательность\n• Желание учиться"
    )

async def start_survey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "1️⃣ Почему вы выбрали направление стоматологии?",
        reply_markup=survey_keyboard
    )
    return Q1

async def ask_next(update, context, question_text, next_state, key):
    context.user_data[key] = update.message.text
    await update.message.reply_text(question_text, reply_markup=survey_keyboard)
    return next_state

# -----------------------
# Вопросы опросника
# -----------------------
async def q1(update, context): return await ask_next(update, context, "2️⃣ В каком возрасте и при каких обстоятельствах вы приняли решение поступать в медицинский вуз/колледж?", Q2, "q1")
async def q2(update, context): return await ask_next(update, context, "3️⃣ Почему вы выбрали именно ортодонтию как профиль? Что вас в ней привлекает?", Q3, "q2")
async def q3(update, context): return await ask_next(update, context, "4️⃣ Какие профессиональные цели вы ставите перед собой на ближайшие 3–5 лет?", Q4, "q3")
async def q4(update, context): return await ask_next(update, context, "5️⃣ На какую зарплату вы рассчитываете?", Q5, "q4")
async def q5(update, context): return await ask_next(update, context, "6️⃣ Какое у вас образование? (вуз/колледж, специальность, год окончания)", Q6, "q5")
async def q6(update, context): return await ask_next(update, context, "7️⃣ Проходили ли вы дополнительные курсы или обучающие программы по стоматологии или ортодонтии?", Q7, "q6")
async def q7(update, context): return await ask_next(update, context, "8️⃣ Какой опыт работы у вас уже есть в сфере стоматологии?", Q8, "q7")
async def q8(update, context): return await ask_next(update, context, "9️⃣ Есть ли опыт работы в качестве ассистента ортодонта или на близкой позиции?", Q9, "q8")
async def q9(update, context): return await ask_next(update, context, "10️⃣ Какие практические навыки вы уже освоили?", Q10, "q9")
async def q10(update, context): return await ask_next(update, context, "11️⃣ Есть ли навыки общения с пациентами, особенно с детьми и подростками?", Q11, "q10")
async def q11(update, context): return await ask_next(update, context, "12️⃣ Какие программы или клинические системы вы умеете использовать?", Q12, "q11")
async def q12(update, context): return await ask_next(update, context, "13️⃣ Какие свои качества вы считаете особенно важными для работы в ортодонтии?", Q13, "q12")
async def q13(update, context): return await ask_next(update, context, "14️⃣ Как вы реагируете на стрессовые или нестандартные ситуации?", Q14, "q13")
async def q14(update, context): return await ask_next(update, context, "15️⃣ Какой стиль работы вам ближе: строгие инструкции или работа с элементами самостоятельности?", Q15, "q14")
async def q15(update, context): return await ask_next(update, context, "16️⃣ Готовы ли вы к обучению новым техникам и протоколам?", Q16, "q15")
async def q16(update, context): return await ask_next(update, context, "17️⃣ Что для вас наиболее важно в работе — профессиональный рост, стабильность, коллектив, график, зарплата?", Q17, "q16")

async def q17(update, context):
    context.user_data["q17"] = update.message.text
    await update.message.reply_text("Спасибо за ваши ответы! 🤝", reply_markup=ReplyKeyboardRemove())
    summary = "\n".join([f"{i+1}. {context.user_data[f'q{i+1}']}" for i in range(17)])
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"Новый опрос:\n\n{summary}")
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Опрос отменён.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# -----------------------
# Основная функция
# -----------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("Начать опрос"), start_survey)],
        states={i: [MessageHandler(filters.TEXT & ~filters.COMMAND, globals()[f"q{i+1}"])] for i in range(17)},
        fallbacks=[MessageHandler(filters.Regex("Отмена"), cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("О вакансии"), info))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()
