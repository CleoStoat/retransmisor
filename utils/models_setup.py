from telegram.ext import CallbackContext


async def setup_models(context: CallbackContext) -> None:
    if "chats" not in context.bot_data:
        context.bot_data["chats"] = []

    if "mensajes" not in context.bot_data:
        context.bot_data["mensajes"] = []
