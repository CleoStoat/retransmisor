import logging

import config
from models.chat import Chat
from models.mensaje import Mensaje, generar_codigo, validar_horario
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "borrar_msg"
DESCRIPTION = "Borra un mensaje programado"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return
    if not context.args:
        await update.message.reply_text("Error. Dame el codigo del mensaje.")
        return

    codigo = context.args[0]

    mensaje_encontrado = [
        msg for msg in context.bot_data["mensajes"] if str(msg.codigo) == codigo
    ]

    if not mensaje_encontrado:
        await update.message.reply_text("Error. No se encontró el mensaje con ese código.")
        return

    mensaje: Mensaje = mensaje_encontrado[0]

    context.bot_data["mensajes"].remove(mensaje)
    await update.message.reply_text("Mensaje borrado.")


