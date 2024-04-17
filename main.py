from dotenv import load_dotenv
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler, \
    MessageHandler, filters
from data import db_session, Prediction, Cards

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

MAIN, GADANIYA, NAME, PURPOSE, QUESTION, READY = range(6)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton('Гадаем', callback_data=str(GADANIYA))
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, PODRUGA!\n"
             "Если ты нашла этот бот, то наша команда PODRUGA - единственный выход из твой ситуации!\n\n"
             "Знай, мы с тобой!\n"
             "PODRUGA, не упусти возможность стать частью НАС!",
        reply_markup=reply_markup
    )


async def gadania_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = '''Ты попала в инновационную систему гадания POGRUGA S TARO
    
Для начала скажи мне, как тебя зовут, PODRUGA?'''
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data['name'] = text
    keyboard = [
        ["Мой день"],
        ["Любовь"],
        ["Карьера"],
        ["Да/Нет"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Выбери категорию"
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Выбери категорию, которая соответствует запросу твоего гадания",
        reply_markup=reply_markup
    )
    return PURPOSE


async def get_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data['purpose'] = text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Введи свой конкретный запрос ИЛИ '-' чтобы пропустить"
    )
    return QUESTION


async def skip_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["ДА", "ЕЩЕ КАК"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Готова?"
    )

    with open('izn_card.jpg', "rb") as photo:
        await context.bot.send_photo(
            photo=photo,
            chat_id=update.effective_chat.id,
            caption=f"Приложи палец к карте, заряжаем колоду твоей энергией\n\nГотова?",
            reply_markup=reply_markup
        )
    return  READY


async def get_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data['question'] = text
    keyboard = [
        ["ДА", "ЕЩЕ КАК"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Готова?"
    )
    with open('izn_card.jpg', "rb") as photo:
        await context.bot.send_photo(
            photo=photo,
            chat_id=update.effective_chat.id,
            caption=f"Приложи палец к карте, заряжаем колоду твоей энергией\n\nГотова?",
            reply_markup=reply_markup
        )
    return  READY


async def gadat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    session = db_session.create_session()
    preds = session.query(Prediction).all()
    for pred in preds:
        print(pred.day)



if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(gadania_start, pattern=f'^{str(GADANIYA)}$')],
        states={
            NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
            PURPOSE: [MessageHandler(filters.Regex('^(Мой день|Любовь|Карьера|Да/Нет)$'), get_purpose)],
            QUESTION: [
                MessageHandler(filters.Regex('^-$'), skip_answer),
                MessageHandler(filters.TEXT & (~filters.COMMAND) & (~filters.Regex('^-$')), get_question)
            ],
            READY: [MessageHandler(filters.Regex('^ДА|ЕЩЁ КАК$'), gadat)]
        },
        fallbacks=[CallbackQueryHandler(gadania_start, pattern=f'^{str(GADANIYA)}$')]
    )

    application.add_handler(CommandHandler('start', start))

    application.add_handler(conv_handler)

    db_session.global_init("./db/gadalka.db")

    session = db_session.create_session()
    preds = session.query(Prediction).filter()
    for pred in preds:
        print(pred.day)


    application.run_polling()


