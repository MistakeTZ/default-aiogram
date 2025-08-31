from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from tasks.loader import dp, bot, sender
from os import path

from tasks.config import get_env, get_config
import tasks.kb as kb
from tasks.states import UserState
from database.model import users
import logging


# Команда старта бота
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    if not users.filter(telegram_id=user_id).one():
        logging.info(f"New user: {user_id}")
        users.insert(telegram_id=user_id, name=msg.from_user.full_name, username=msg.from_user.username)

    await sender.message(user_id, "start")
    await state.set_state(UserState.default)
