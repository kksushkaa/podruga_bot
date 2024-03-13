from dotenv import load_dotenv
import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет, PODRUGA!\n"
             "Если ты нашла этот бот, то наша команда PODRUGA - единственный выход из твой ситуации.\n\n"
             "Знай, мы с тобой!\n"
             "PODRUGA, не упусти возможность стать частью НАС!")


if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TOKEN')).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    application.run_polling()