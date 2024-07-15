from aiogram import F
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp, bot
import asyncio
from os import path

from config import get_env, get_config

import utils.kb as kb
from support.messages import get_text, send_message
from states import UserState


# Возвращение в меню
@dp.callback_query(F.data == "back")
async def menu_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    await send_message(clbck.message, "menu", None, state, UserState.default)


# Начинается с
@dp.callback_query(F.data.startswith("start_"))
async def city_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    answer = clbck.data[-1] == "y"
