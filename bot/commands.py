from icmplib import ping
from telegram import Update
from telegram.ext import ContextTypes

from .messages import error_message, ping_message, triggers_message
from .parsers import parse_ping_command, parse_ping_reply_command
from .zabbix import get_triggers

PING_COUNT_MAX = 100


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

    try:
        await update.message.reply_text(triggers_message(get_triggers()))
    except Exception as e:
        await update.message.reply_text(error_message(e))


async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return

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
