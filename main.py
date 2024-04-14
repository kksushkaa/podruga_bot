from dotenv import load_dotenv
import os
import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ConversationHandler, CallbackQueryHandler, \
    MessageHandler, filters
from data import db_session, Prediction, Cards
import random

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
        [
            InlineKeyboardButton('Рецепты', callback_data='2')
        ]
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
        ["ДА", "ЕЩЁ КАК"]
    ]
    text = update.effective_message.text
    context.user_data['question'] = text
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Готова?"
    )

    with open('img/izn_card.jpg', "rb") as photo:
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
        ["ДА", "ЕЩЁ КАК"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Готова?"
    )
    with open('img/izn_card.jpg', "rb") as photo:
        await context.bot.send_photo(
            photo=photo,
            chat_id=update.effective_chat.id,
            caption=f"Приложи палец к карте, заряжаем колоду твоей энергией\n\nГотова?",
            reply_markup=reply_markup
        )
    return READY


async def gadat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    session = db_session.create_session()
    n = random.randint(1, 22)
    card = session.query(Cards).filter(Cards.id == n).first()
    prediction = session.query(Prediction).filter(Prediction.id == n).first()
    print(context.user_data['name']) #Ксюша
    print(context.user_data['purpose']) #Словами
    print(context.user_data['question'])
    text = f'{context.user_data['name']}, Podruga. Наша система определила'
    if context.user_data['question'] != '-':
        text += f', что ответ на твой вопрос "{context.user_data['question']}":\n'
    else:
        text += f', что ответ на ваше секретное душевное переживание.\n'
    if context.user_data['purpose'] == 'Мой день':
        prediction_text = prediction.day
        text += f"```\n{prediction_text}\n```"
    elif context.user_data['purpose'] == 'Любовь':
        prediction_text = prediction.love
        text += f"```\n{prediction_text}\n```"
    elif context.user_data['purpose'] == 'Карьера':
        prediction_text = prediction.career
        text += f"```\n{prediction_text}\n```"
    elif context.user_data['purpose'] == 'Да/Нет':
        prediction_text = card.yes_no_pred
        text += f"```\n{prediction_text}\n```"

    text += f'\nПотому что выпала *карта*\\: *{card.card_name}*\n'
    text += f'__Podruga, оцени наш ответ на твой запрос__'
    text = text.replace('.','\\.')
    text = text.replace(',', '\\,')
    text = text.replace('!', '\\!')
    text = text.replace('?', '\\?')
    keyboard = [
        [
            InlineKeyboardButton('1', callback_data="1_score"),
            InlineKeyboardButton('2', callback_data="2_score"),
            InlineKeyboardButton('3', callback_data="3_score"),
            InlineKeyboardButton('4', callback_data="4_score"),
            InlineKeyboardButton('5', callback_data="5_score"),
        ]
    ]
    with open(f'img/{card.image}', 'rb') as photo:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo, caption=text, parse_mode="MarkdownV2", reply_markup=InlineKeyboardMarkup(keyboard))






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
            READY: [MessageHandler(filters.Regex('^(ДА|ЕЩЁ КАК)$'), gadat)]
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


