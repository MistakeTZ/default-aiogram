import logging

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.model import User
from tasks import kb
from tasks.config import get_config
from tasks.loader import dp, sender, session
from tasks.states import UserState


@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    user = session.query(User).filter_by(telegram_id=user_id).one_or_none()

    if not user:
        logging.info(f"New user: {user_id}")
        user = User(
            telegram_id=user_id,
            name=msg.from_user.full_name,
            username=msg.from_user.username,
        )
        if user_id in get_config("admins"):
            user.role = "admin"
        session.add(user)
        session.commit()

    await sender.message(user_id, "start")
    await state.set_state(UserState.default)
