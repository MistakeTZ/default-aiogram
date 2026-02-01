from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy import exists

from database.model import User
from tasks.loader import dp, sender, session


class Restricted(Filter):
    async def __call__(self, message):
        return session.query(
            exists().where(
                User.telegram_id == message.from_user.id,
                User.restricted,
            )
        ).scalar()


# Команда бана
@dp.message(Restricted())
async def ban_handler(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    await sender.message(user_id, "you_banned")
