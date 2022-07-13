import logging

import config
from models.chat import Chat
from models.mensaje import Mensaje, generar_codigo, validar_horario
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger()

NAME = "repetir"
DESCRIPTION = "Repetir un mensaje en un chat con horario"


async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id != config.BOT_OWNER_ID:
        await update.message.reply_text("No eres dios.")
        return
    if not context.args:
        await update.message.reply_text("Error. Dame el id del chat.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Error. Dame el horario en el cual repetir el mensaje"
        )
        return

    id_chat = context.args[0]
    horario = context.args[1]

    if not validar_horario(horario):
        await update.message.reply_text(
            "Error. El horario no tiene el formato correcto."
        )
        return

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

    message_id = await context.bot.copy_message(
        chat_id=config.BOT_OWNER_ID,
        from_chat_id=update.effective_chat.id,
        message_id=mensaje.id,
        reply_markup=mensaje.reply_markup,
    )

    id_mensaje_copiado = message_id.message_id

    mensaje_guardado = Mensaje(
        id_chat=id_chat,
        id_mensaje=id_mensaje_copiado,
        horario=horario,
        codigo=generar_codigo(context.bot_data["mensajes"]),
        botones=mensaje.reply_markup,
    )

    context.bot_data["mensajes"].append(mensaje_guardado)

    await update.message.reply_text(
        f"Mensaje programado para {horario} con código {mensaje_guardado.codigo}."
    )
