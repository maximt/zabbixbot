import os

from commands import help_command, list_command, menu_commands, ping_command
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(commands=menu_commands)


def main() -> None:
    if not TELEGRAM_TOKEN:
        raise ValueError("TELEGRAM_TOKEN is not set")

    application = (
        Application.builder().token(TELEGRAM_TOKEN).post_init(post_init).build()
    )

    application.add_handler(CommandHandler("list", list_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
