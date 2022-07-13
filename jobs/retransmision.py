import datetime
from distutils.command.config import config

import config
from models.mensaje import Mensaje
from models.chat import Chat
from telegram.ext import ContextTypes


def es_hora(horario: str) -> bool:
    hora_actual = datetime.datetime.now().hour
    min_actual = datetime.datetime.now().minute

    hora_msg, min_msg = [int(x) for x in horario.split("-")[1].split(":")]

    return hora_msg == hora_actual and min_msg == min_actual


def es_dia(horario: str) -> bool:
    letras_dias = ["L", "M" "X" "J", "V", "S", "D"]
    num_dia_actual = datetime.datetime.today().weekday()

    letra_dia_actual = letras_dias[num_dia_actual]

    letra_horario = horario.split("-")[0]

    return letra_horario == letra_dia_actual or letra_horario == "*"


async def retransmision_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    mensajes: list[Mensaje] = context.bot_data["mensajes"]

    for mensaje in mensajes:
        horario = mensaje.horario
        # Buscar chat
        chat_encontrado = [chat for chat in context.bot_data["chats"] if str(chat.id_chat) == mensaje.id_chat]
        chat: Chat = chat_encontrado[0]

        if not chat.autorizado:
            continue

        if es_dia(horario) and es_hora(horario):

            try:
                # reenviar mensaje
                await context.bot.copy_message(
                    chat_id=mensaje.id_chat,
                    from_chat_id=config.BOT_OWNER_ID,
                    message_id=mensaje.id_mensaje,
                    reply_markup=mensaje.botones,
                )
            except Exception:
                continue