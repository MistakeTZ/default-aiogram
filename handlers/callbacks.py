from maxapi import F
from maxapi.types import MessageCallback
from maxapi.context import MemoryContext

from tasks import kb
from tasks.loader import dp, sender
from tasks.states import UserState


# Возвращение в меню
@dp.message_callback(F.callback.payload == "back")
async def menu_handler(event: MessageCallback, context: MemoryContext) -> None:
    await sender.edit_message(event.message, "menu")
    await context.clear()
