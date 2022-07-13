import logging

import config
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()
NAME = "desautorizar"
DESCRIPTION = "Desautorizar un chat con su id"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return
    if not context.args:
        await update.message.reply_text("Error. Dame el id del chat.")
        return

    id_chat = context.args[0]

    # Buscar id en base de datos
    chat_encontrado = [
        chat for chat in context.bot_data["chats"] if str(chat.id_chat) == id_chat
    ]

    if not chat_encontrado:
        await update.message.reply_text(
            "Error. El bot no ha sido agregado al chat aún."
        )
        return

    chat_encontrado[0].autorizado = False
    chat = chat_encontrado[0]
    await update.message.reply_text(
        f"Chat {chat.nombre} (id: {chat.id_chat}) desautorizado"
    )
