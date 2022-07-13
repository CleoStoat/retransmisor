import logging

import config
from models.chat import Chat
from models.mensaje import Mensaje, generar_codigo, validar_horario
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "lista_msgs"
DESCRIPTION = "Muestra una lista de todos los mensjaes programado"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return
    mensajes: list[Mensaje] = context.bot_data["mensajes"]

    text = "Listado de mensajes:\n"
    for mensaje in mensajes:
        chat_encontrado = [
            chat
            for chat in context.bot_data["chats"]
            if str(chat.id_chat) == mensaje.id_chat
        ]
        chat: Chat = chat_encontrado[0]

        text += f"> Chat: {chat.nombre} Id chat: {mensaje.id_chat} Horario: {mensaje.horario} Codigo: {mensaje.codigo}\n"

    await update.effective_message.reply_text(text)
