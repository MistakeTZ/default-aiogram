from aiogram import F
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp
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


# Выбран город
@dp.callback_query(F.data.startswith("choose_city_"))
async def city_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    city = clbck.data[12:]
    if city != "other":
        await send_message(clbck.message, "city_chosen", None, None, None, get_config("cities", city, "name"))