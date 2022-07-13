import logging

import config
from models.chat import Chat
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "lista_chats"
DESCRIPTION = "Lista todos los chats donde fue agregado"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return

    # Buscar id en base de datos
    chats_autorizados: list[Chat] = [
        chat for chat in context.bot_data["chats"] if chat.autorizado
    ]
    chats_no_autorizados = [
        chat for chat in context.bot_data["chats"] if not chat.autorizado
    ]

    text = "Chats autorizados:\n"
    for chat in chats_autorizados:
        text += f"Chat: {chat.nombre} - id: {chat.id_chat}\n"
    text += "\nChats no autorizados:\n"
    for chat in chats_no_autorizados:
        text += f"Chat: {chat.nombre} - id: {chat.id_chat}\n"

    await update.message.reply_text(text)
