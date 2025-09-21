from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from tasks.loader import dp, bot, sender, session, User
from sqlalchemy import exists

from tasks.config import get_env, get_config
from tasks.states import UserState
import logging


@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    
    if not session.query(exists().where(User.telegram_id == user_id)).scalar():
        logging.info(f"New user: {user_id}")
        user = User(telegram_id=user_id, name=msg.from_user.full_name, username=msg.from_user.username)
        if user_id in get_config("admins"):
            user.role = "admin"
        session.add(user)
        session.commit()

    await sender.message(user_id, "start")
    await state.set_state(UserState.default)
