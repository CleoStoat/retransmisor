import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "start"
DESCRIPTION = "This is the command to start the bot"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("This is the start command")
