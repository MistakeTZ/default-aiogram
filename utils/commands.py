from aiogram import F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp, bot
from os import path

from config import get_env, update_config
import utils.kb as kb
from support.messages import message, send_message
from states import UserState


# Команда старта бота
@dp.message(CommandStart())
async def command_start_handler(msg: Message, state: FSMContext) -> None:
    id = msg.from_user.id
    print(id)
    await send_message(msg, "greetings", kb.cities(), state, UserState.default)


# Команда настроек
@dp.message(Command("settings"))
async def command_settings(msg: Message, state: FSMContext) -> None:
    await message(msg, "settings", kb.cities())

    