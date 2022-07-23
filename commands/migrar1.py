import logging
import pickle

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "migrar1"
DESCRIPTION = "This is the command to start the bot"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("migracion1", mode="wb") as f:
        pickle.dump(context.bot_data, f, protocol=pickle.HIGHEST_PROTOCOL)

    await update.message.reply_text("Migracion parte 1 completa")
