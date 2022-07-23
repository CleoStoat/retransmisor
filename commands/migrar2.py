import logging
import pickle

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "migrar2"
DESCRIPTION = "This is the command to start the bot"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    with open("migracion1", mode="rb") as f:
        bot_data = pickle.load(f)
        
        context.bot_data["mensajes"] = bot_data["mensajes"]
        context.bot_data["chats"] = bot_data["chats"]

    await update.message.reply_text("Migracion parte 2 completa")
