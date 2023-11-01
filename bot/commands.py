from icmplib import ping
from messages import error_message, help_message, ping_message, triggers_message
from parsers import parse_ping_command, parse_ping_reply_command
from telegram import BotCommand, Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes
from zabbix import get_triggers

PING_COUNT_MAX = 100


menu_commands = [
    BotCommand("list", "List of problems"),
    BotCommand("help", "Usage information"),
]


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )

    try:
        await update.message.reply_html(triggers_message(get_triggers()))
    except Exception as e:
        await update.message.reply_text(error_message(e))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )

    try:
        await update.message.reply_text(help_message())
    except Exception as e:
        await update.message.reply_text(error_message(e))


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    await context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=ChatAction.TYPING
    )

    try:
        if update.message.reply_to_message:
            hostname, count = parse_ping_reply_command(
                str(update.message.text), str(update.message.reply_to_message.text)
            )
        else:
            hostname, count = parse_ping_command(str(update.message.text))

        count = max(1, min(count, PING_COUNT_MAX))
        pong = ping(hostname, count=count, privileged=False)
        await update.message.reply_text(ping_message(pong))
    except Exception as e:
        await update.message.reply_text(error_message(e))
