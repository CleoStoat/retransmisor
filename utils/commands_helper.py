import dataclasses
import importlib
import os
from typing import Callable

from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler, ContextTypes


@dataclasses.dataclass
class Command:
    func: Callable[[Update, ContextTypes.DEFAULT_TYPE], None]
    name: str
    description: str


def get_commands_list() -> list[Command]:
    command_module_names = [
        module.split(".")[0]
        for module in os.listdir("./commands")
        if module.endswith("py") and not module.startswith("__init__")
    ]

    commands = []

    for cmd_mod_name in command_module_names:
        cmd_module = importlib.import_module("commands." + cmd_mod_name)
        cmd = Command(
            func=cmd_module.command,
            name=cmd_module.NAME,
            description=cmd_module.DESCRIPTION,
        )
        commands.append(cmd)

    return commands


async def set_bot_commands(context: CallbackContext) -> None:
    application: Application = context.application
    
    commands = get_commands_list()
    for command in commands:
        application.add_handler(CommandHandler(command.name, command.func))

    await application.bot.set_my_commands(
        [(command.name, command.description) for command in commands]
    )
