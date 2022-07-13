import logging

from telegram import Update
from telegram.ext import ContextTypes
import config
logger = logging.getLogger()

NAME = "help"
DESCRIPTION = "This is the command to get help"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return
    
    await update.message.reply_text("Aquí iría el listado de comandos...")
