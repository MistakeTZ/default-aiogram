from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from loader import dp

import os
from config import get_env
import re
import asyncio

import utils.kb as kb
from support.messages import message, send_message, get_text
from states import UserState


# Установка электронной почты
@dp.message(UserState.email)
async def profile(msg: Message, state: FSMContext):
    if not re.fullmatch("([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+", msg.text):
        await send_message(msg, "wrong_email")
        return
    await send_message(msg, "thx")
    await asyncio.sleep(1)
    await send_message(msg, "what_course_is")
    await asyncio.sleep(5)
    await send_message(msg, "lets_begin", kb.two_buttons("start_course_go", "start_course_go", "start_course_no", "start_course_no"), state, UserState.default)


# Изменение города
@dp.message(UserState.write_city)
async def profile(msg: Message, state: FSMContext):
    if len(msg.text) < 255:
        await send_message(msg, "fixed_city")
        await send_message(msg, "begin", kb.link_button(1)) 
        await send_message(msg, "when_end", kb.buttons("ended", "task"), state, UserState.default) 
