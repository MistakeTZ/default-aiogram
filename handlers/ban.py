from aiogram import F
from aiogram.filters import Filter, Command
from database.model import DB
from tasks.loader import sender, dp
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class Restricted(Filter):
    async def __call__(self, message):
        user = DB.get("select id from users where telegram_id = ? and \
                      restricted = 1", [message.from_user.id], True)
        return bool(user)


# Команда бана
@dp.message(Restricted())
async def ban_handler(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    await sender.message(user_id, "you_banned")
