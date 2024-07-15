from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from loader import dp, bot
from datetime import datetime

from os import path
import re
from config import get_env
import asyncio

import utils.kb as kb
from support.messages import send_message, get_text
from states import UserState


# Установка электронной почты
@dp.message(UserState.email)
async def email_check(msg: Message, state: FSMContext):
    email_regex = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    if not re.fullmatch(email_regex, msg.text):
        await send_message(msg, "wrong_email")
        return
    pass


# Установка времени
@dp.message(UserState.time)
async def time_check(msg: Message, state: FSMContext):
    try:
        time = datetime.strptime(msg.text, "%H:%M")
    except:
        await send_message(msg, "wrong_time")
        return



# Установка телефона
@dp.message(UserState.phone)
async def phone_check(msg: Message, state: FSMContext):
    if msg.contact:
        phone = msg.contact.phone_number
    else:
        if is_valid_phone_number(msg.text):
            phone = msg.text
        else:
            await send_message(msg, "wrong_phone")
            return


def is_valid_phone_number(phone):
    pattern = r'^(?:8|\+7)\d{10}$'
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    return bool(re.match(pattern, cleaned_phone))
