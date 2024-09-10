from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp, bot, sender
from os import path
from datetime import datetime

from config import get_env, get_config
import utils.kb as kb
from states import UserState
from database.model import DB


# Команда старта бота
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    id = msg.from_user.id
    if not DB.select(id):
        print("New user:", id)
        DB.commit("insert into users (telegram_id, registered) values (?, ?)", [id, datetime.now()])

    await sender.send_message(id, "start")
    await state.set_state(UserState.default)


# Команда меню
@dp.message(Command("menu"))
async def command_settings(msg: Message, state: FSMContext) -> None:
    id = msg.from_user.id
    await sender.send_message(id, "menu")
    await state.set_state(UserState.default)
    