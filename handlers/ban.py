from aiogram import F
from aiogram.filters import Filter, Command
from database.model import users
from tasks.loader import sender, dp
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class Restricted(Filter):
    async def __call__(self, message):
        user = users.filter(telegram_id=message.from_user.id, restricted=1).one()
        return bool(user)


# Команда бана
@dp.message(Restricted())
async def ban_handler(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    await sender.message(user_id, "you_banned")
