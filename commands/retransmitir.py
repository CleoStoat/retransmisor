import logging

import config
from models.chat import Chat
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "retransmitir"
DESCRIPTION = "Retransmite un mensaje al canal que me digas su id"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return
    if not context.args:
        await update.message.reply_text("Error. Dame el id del chat.")
        return

    id_chat = context.args[0]

    # Buscar id en base de datos
    chat_encontrado: list[Chat] = [
        chat for chat in context.bot_data["chats"] if str(chat.id_chat) == id_chat
    ]

    if not chat_encontrado:
        await update.message.reply_text(
            "Error. El bot no ha sido agregado al chat aún."
        )
        return

    chat = chat_encontrado[0]

    if not chat.autorizado:
        await update.message.reply_text(
            "Error. El bot no ha sido autorizado en ese chat."
        )
        return

    if update.effective_message.reply_to_message is None:
        await update.message.reply_text(
            "Error. Tienes que responder al mensaje que quieras retransmitir."
        )
        return

    mensaje = update.effective_message.reply_to_message

    await context.bot.copy_message(
        chat_id=id_chat,
        from_chat_id=update.effective_chat.id,
        message_id=mensaje.id,
        reply_markup=mensaje.reply_markup,
    )

    await update.message.reply_text("Retransmitido.")
