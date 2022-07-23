import logging

import config
from models.chat import Chat
from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown

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

    text = escape_markdown("Chats autorizados:\n")
    for chat in chats_autorizados:
        aux = escape_markdown(f"Chat: {chat.nombre} - id: ")
        text += f"{aux}`{escape_markdown(str(chat.id_chat))}`"
        text += escape_markdown('\n')
    text += escape_markdown("\nChats no autorizados:\n")
    for chat in chats_no_autorizados:
        aux = escape_markdown(f"Chat: {chat.nombre} - id: ")
        text += f"{aux}`{escape_markdown(str(chat.id_chat))}`"
        text += escape_markdown('\n')

    print(text)

    await update.message.reply_text(text, parse_mode="MarkdownV2")
