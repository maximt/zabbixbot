import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler

from bot.commands import list_command, ping_command

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("ping", ping_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
