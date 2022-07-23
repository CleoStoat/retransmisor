import sys

from datetime import timedelta
import logging

from telegram.ext import Application, MessageHandler, filters, ChatMemberHandler

import config
from models.chat import Chat
from persistence import SQLAlchemyPersistence
from utils.commands_helper import set_bot_commands
from utils.models_setup import setup_models
from telegram.helpers import escape_markdown

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, PicklePersistence

from jobs.retransmision import retransmision_job

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def chatmemeberhandler(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # Guardar id del canal
    id_chat = update.effective_chat.id
    tipo_chat = update.effective_chat.type.value
    nombre_chat = update.effective_chat.title

    user_fullname = update.effective_user.full_name
    user_username = update.effective_user.name
    user_id = update.effective_user.id
    user_link = update.effective_user.link

    status_chat = update.my_chat_member.new_chat_member.status

    text = f"Chat {tipo_chat}\n"
    text += f"Status chat: {status_chat}\n"

    text += f"Nombre chat: {nombre_chat}\n"
    text = escape_markdown(text, 2)
    text += f"Id: `{escape_markdown(str(id_chat), 2)}`\n"

    text2 = f"Nombre user: {user_fullname}\n"
    text2 += f"Username user: {user_username}\n"
    text2 += f"Id user: {user_id}\n"
    text2 = escape_markdown(text2, 2)
    text2 += f"Link user: [{escape_markdown(str(user_fullname), 2)}]({escape_markdown(str(user_link), 2)})\n"
    text += text2

    await context.bot.send_message(
        chat_id=config.BOT_OWNER_ID, text=text, parse_mode="MarkdownV2"
    )

    chat_encontrado = [
        chat for chat in context.bot_data["chats"] if chat.id_chat == id_chat
    ]

    if chat_encontrado:
        return

    # Agregar el chat a la base de datos
    context.bot_data["chats"].append(
        Chat(id_chat=id_chat, nombre=nombre_chat, autorizado=False)
    )

def main() -> None:
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .persistence(PicklePersistence("db"))
        .build()
    )

    application.job_queue.run_once(callback=set_bot_commands, when=1, data=application)
    application.job_queue.run_once(callback=setup_models, when=1)

    application.job_queue.run_repeating(
        callback=retransmision_job, interval=timedelta(minutes=1), first=1
    )

    application.add_handler(ChatMemberHandler(callback=chatmemeberhandler))

    application.run_polling()

def mainold() -> None:
    sqlite_name = "newdb.db"
    sqlite_url = "sqlite:///./" + sqlite_name
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .persistence(SQLAlchemyPersistence(url=sqlite_url))
        .build()
    )

    application.job_queue.run_once(callback=set_bot_commands, when=1, data=application)
    application.job_queue.run_once(callback=setup_models, when=1)

    application.job_queue.run_repeating(
        callback=retransmision_job, interval=timedelta(minutes=1), first=1
    )

    application.add_handler(ChatMemberHandler(callback=chatmemeberhandler))

    application.run_polling()


if __name__ == "__main__":
    if sys.argv > 1:
        mainold()
    else:
        main()

