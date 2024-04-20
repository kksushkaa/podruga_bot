from dotenv import load_dotenv
import os
import logging
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
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

# состония, использованные в проекте
(
    MAIN,
    GADANIYA,
    NAME,
    PURPOSE,
    QUESTION,
    READY,
    RESULT,
    GET_ADDRESS,
    GET_ADDRESS_CAFE,
    GOLD_APPLE,
    STAR_COFFEE,
) = range(11)


# стартовая фукция
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # кнопки выбора действий
    keyboard = [
        [InlineKeyboardButton("Гадаем", callback_data=str(GADANIYA))],
        [InlineKeyboardButton("Новинка в ЗОЛОТОМ ЯБЛОКЕ", callback_data=str(GOLD_APPLE))],
        [InlineKeyboardButton("Новинка в Stars Coffee", callback_data=str(STAR_COFFEE))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # начальное текстовое сообщение
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, PODRUGA!\n"
             "Если ты нашла этот бот, то наша команда PODRUGA - единственный выход из твой ситуации!\n\n"
             "Знай, мы с тобой!\n"
             "PODRUGA, не упусти возможность стать частью НАС!",
        reply_markup=reply_markup,
    )


# функия начала гадания
async def gadania_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # текст-введение
    text = """Ты попала в инновационную систему гадания POGRUGA S TARO

Для начала скажи мне, как тебя зовут, PODRUGA?"""
    # получение имени
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return NAME


# функция новинок в золотом яблоке в зависимости от введенного адреса
async def new_products_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """Введите свой адрес"""
    # получение адреса
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return GET_ADDRESS


# функция новинок в старс кофе в зависимости от введенного адреса
async def new_drinks_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """Введите свой адрес"""
    # получение адреса
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    return GET_ADDRESS_CAFE


# функция выбора категории гадания
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data["name"] = text
    # выбор категории
    keyboard = [["Мой день"], ["Любовь"], ["Карьера"], ["Да/Нет"]]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Выбери категорию",
    )
    # текст для выбора категории
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Выбери категорию, которая соответствует запросу твоего гадания",
        reply_markup=reply_markup,
    )
    return PURPOSE


# функция получения адреса зя
async def get_shop_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data["address"] = text
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    import requests
    import sqlite3

    # обращение к бд
    products = sqlite3.connect("new_product.db")
    cursor = products.cursor()
    cursor.execute("SELECT * FROM shop_products")
    shop_prod = cursor.fetchall()

    address = text

    # работа с адресом
    if address == "" or address.count(" ") == len(address):
        pass
    else:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey=b2f42f9a-efc2-4a51-b051-5dbd204fa768&geocode={address}&format=json"

        r = requests.get(url)

        geo_code = r.json()
        coordinates = geo_code["response"]
        coordinates_1 = coordinates["GeoObjectCollection"]
        coordinates_2 = coordinates_1["featureMember"]
        coordinates_3 = coordinates_2[0]
        coordinates_4 = coordinates_3["GeoObject"]
        coordinates_5 = coordinates_4["Point"]
        coordinates_6 = coordinates_5["pos"]
        coordinates_6_1 = coordinates_6.split()
        latitude = float(coordinates_6_1[0])
        longitude = float(coordinates_6_1[1])
        # print(latitude, longitude)

        min_range = 1000000000000000000
        shop_data = []

        for e in shop_prod:
            vec = (e[4] - latitude) ** 2 + (e[5] - longitude) ** 2
            vec1 = vec ** 0.5
            if vec1 < min_range:
                min_range = vec1
                shop_data = e

        # выбор фото по соответствующему адресу
        with open(f"products_photo/{shop_data[3]}", "rb") as photo:
            await context.bot.send_photo(
                photo=photo,
                chat_id=update.effective_chat.id,
                caption=f"Адрес: {shop_data[2]}",
            )
    await start(update, context)
    return ConversationHandler.END


# функция получения адреса старс
async def get_cafe_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data["address"] = text
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

    import requests
    import sqlite3

    # обращение к бд
    drinks = sqlite3.connect("stars.db")
    cursor = drinks.cursor()
    cursor.execute("SELECT * FROM cafe_drink")
    shop_prod = cursor.fetchall()

    address = text

    # работа с адресом
    if address == "" or address.count(" ") == len(address):
        pass
    else:
        url = f"https://geocode-maps.yandex.ru/1.x/?apikey=b2f42f9a-efc2-4a51-b051-5dbd204fa768&geocode={address}&format=json"
        r = requests.get(url)

        geo_code = r.json()
        coordinates = geo_code["response"]
        coordinates_1 = coordinates["GeoObjectCollection"]
        coordinates_2 = coordinates_1["featureMember"]
        coordinates_3 = coordinates_2[0]
        coordinates_4 = coordinates_3["GeoObject"]
        coordinates_5 = coordinates_4["Point"]
        coordinates_6 = coordinates_5["pos"]
        coordinates_6_1 = coordinates_6.split()
        latitude = float(coordinates_6_1[0])
        longitude = float(coordinates_6_1[1])
        # print(latitude, longitude)

        min_range = 1000000000000000000
        shop_data = []

        for e in shop_prod:
            vec = (e[4] - latitude) ** 2 + (e[5] - longitude) ** 2
            vec1 = vec ** 0.5

            if vec1 < min_range:
                min_range = vec1
                shop_data = e

        # выбор фото по соответствующему адресу
        with open(f"products_photo/{shop_data[3]}", "rb") as photo:
            await context.bot.send_photo(
                photo=photo,
                chat_id=update.effective_chat.id,
                caption=f"Адрес: {shop_data[2]}",
            )
    await start(update, context)
    return ConversationHandler.END


# функция для ввода запрос
async def get_purpose(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data["purpose"] = text

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Введи свой конкретный запрос ИЛИ '-' чтобы пропустить",
    )
    return QUESTION


# функция для пропуска запроса
async def skip_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["ДА", "ЕЩЁ КАК"]]
    text = update.effective_message.text
    context.user_data["question"] = text

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Готова?",
    )
    # заряжаем фото энергией
    with open("img/izn_card.jpg", "rb") as photo:
        await context.bot.send_photo(
            photo=photo,
            chat_id=update.effective_chat.id,
            caption=f"Приложи палец к карте, заряжаем колоду твоей энергией\n\nГотова?",
            reply_markup=reply_markup,
        )
    return READY


# выбор фото по соответствующему адресу
async def get_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    context.user_data["question"] = text
    keyboard = [["ДА", "ЕЩЁ КАК"]]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        one_time_keyboard=True,
        resize_keyboard=True,
        input_field_placeholder="Готова?",
    )
    # взятие фото для передачи энергии
    with open("img/izn_card.jpg", "rb") as photo:
        await context.bot.send_photo(
            photo=photo,
            chat_id=update.effective_chat.id,
            caption=f"Приложи палец к карте, заряжаем колоду твоей энергией\n\nГотова?",
            reply_markup=reply_markup,
        )
    return READY


# функция для самого гадания
async def gadat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.effective_message.text
    session = db_session.create_session()
    # выбор карты
    n = random.randint(1, 22)

    card = session.query(Cards).filter(Cards.id == n).first()

    prediction = session.query(Prediction).filter(Prediction.id == n).first()

    print(context.user_data["name"])
    print(context.user_data["purpose"])
    print(context.user_data["question"])

    text = f'{context.user_data["name"]}, Podruga. Наша система определила'
    # при наличии запроса
    if context.user_data["question"] != "-":
        text += f', что ответ на твой вопрос {context.user_data["question"]}:\n'
    else:
        # без запроса
        text += f", что ответ на ваше секретное душевное переживание.\n"
    # тема день
    if context.user_data["purpose"] == "Мой день":
        prediction_text = prediction.day
        text += f"```\n{prediction_text}\n```"

    # тема любовь
    elif context.user_data["purpose"] == "Любовь":
        prediction_text = prediction.love
        text += f"```\n{prediction_text}\n```"

    # тема карьера
    elif context.user_data["purpose"] == "Карьера":
        prediction_text = prediction.career
        text += f"```\n{prediction_text}\n```"
    # тема да/нет
    elif context.user_data["purpose"] == "Да/Нет":
        prediction_text = card.yes_no_pred
        text += f"```\n{prediction_text}\n```"

    # создание финального текста
    text += f"\nПотому что выпала *карта*\\: *{card.card_name}*\n"
    text += f"__Podruga, оцени наш ответ на твой запрос__"
    text = text.replace(".", "\\.")
    text = text.replace(",", "\\,")
    text = text.replace("!", "\\!")
    text = text.replace("?", "\\?")
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="1_score"),
            InlineKeyboardButton("2", callback_data="2_score"),
            InlineKeyboardButton("3", callback_data="3_score"),
            InlineKeyboardButton("4", callback_data="4_score"),
            InlineKeyboardButton("5", callback_data="5_score"),
        ]
    ]
    # фото для карты
    with open(f"img/{card.image}", "rb") as photo:
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo,
            caption=text,
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    return RESULT


# оценка гадания
async def get_score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data[0] == "1":
        text = "Себе единицу поставь, NEPODRUGA!"
    elif query.data[0] == "2":
        text = "Прощай, NEPODRUGA!"
    elif query.data[0] == "3":
        text = "BYE-BYE, NEPODRUGA!"
    elif query.data[0] == "4":
        text = "Все понятно, NEPODRUGA!"
    elif query.data[0] == "5":
        text = "Спасибо, ты настоящая PODRUGA!"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    await start(update, context)

    return ConversationHandler.END


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(gadania_start, pattern=f"^{str(GADANIYA)}$")
        ],
        states={
            NAME: [MessageHandler(filters.TEXT & (~filters.COMMAND), get_name)],
            PURPOSE: [
                MessageHandler(
                    filters.Regex("^(Мой день|Любовь|Карьера|Да/Нет)$"), get_purpose
                )
            ],
            QUESTION: [
                MessageHandler(filters.Regex("^-$"), skip_answer),
                MessageHandler(
                    filters.TEXT & (~filters.COMMAND) & (~filters.Regex("^-$")),
                    get_question,
                ),
            ],
            READY: [MessageHandler(filters.Regex("^(ДА|ЕЩЁ КАК)$"), gadat)],
            RESULT: [CallbackQueryHandler(get_score, pattern=f"^._score$")],
        },
        fallbacks=[
            CallbackQueryHandler(gadania_start, pattern=f"^{str(GADANIYA)}$"),
            CallbackQueryHandler(new_products_start, pattern=f"^{GOLD_APPLE}$"),
            CallbackQueryHandler(new_drinks_start, pattern=f"^{STAR_COFFEE}$"),
        ],
    )
    conv_handler2 = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(new_products_start, pattern=f"^{GOLD_APPLE}$")
        ],
        states={
            GET_ADDRESS: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), get_shop_address)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(gadania_start, pattern=f"^{str(GADANIYA)}$"),
            CallbackQueryHandler(new_products_start, pattern=f"^{GOLD_APPLE}$"),
            CallbackQueryHandler(new_drinks_start, pattern=f"^{STAR_COFFEE}$"),
        ],
    )
    conv_handler3 = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(new_drinks_start, pattern=f"^{STAR_COFFEE}$")
        ],
        states={
            GET_ADDRESS_CAFE: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), get_cafe_address)
            ],
        },
        fallbacks=[
            CallbackQueryHandler(gadania_start, pattern=f"^{str(GADANIYA)}$"),
            CallbackQueryHandler(new_products_start, pattern=f"^{GOLD_APPLE}$"),
            CallbackQueryHandler(new_drinks_start, pattern=f"^{STAR_COFFEE}$"),
        ],
    )

    application.add_handler(CommandHandler("start", start))

    application.add_handler(conv_handler)
    application.add_handler(conv_handler2)
    application.add_handler(conv_handler3)

    db_session.global_init("./db/gadalka.db")

    session = db_session.create_session()
    preds = session.query(Prediction).filter()
    for pred in preds:
        print(pred.day)

    application.run_polling()
