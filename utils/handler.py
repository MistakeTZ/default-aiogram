from aiogram import F
from aiogram.filters import Filter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hlink
from aiogram.fsm.context import FSMContext
from loader import dp, bot, sender
from datetime import datetime

from os import path
import re
from config import get_env, get_config
import asyncio

import utils.kb as kb
from states import UserState


# Установка электронной почты
@dp.message(UserState.email)
async def email_check(msg: Message, state: FSMContext):
    id = msg.from_user.id
    if not msg.entities:
        await sender.send_message(id, "wrong_email")
        return
    email_entity = msg.entities[0]
    if email_entity.type != "email":
        await sender.send_message(id, "wrong_email")
        return
    email = msg.text[email_entity.offset:email_entity.length]


# Установка времени
@dp.message(UserState.time)
async def time_check(msg: Message, state: FSMContext):
    id = msg.from_user.id
    try:
        time = datetime.strptime(msg.text, "%H:%M")
    except:
        await sender.send_message(id, "wrong_time")
        return



# Установка телефона
@dp.message(UserState.phone)
async def phone_check(msg: Message, state: FSMContext):
    id = msg.from_user.id
    if msg.contact:
        phone = msg.contact.phone_number
    else:
        if is_valid_phone_number(msg.text):
            phone = msg.text
        else:
            await sender.send_message(id, "wrong_phone")
            return


# Проверка телефона
def is_valid_phone_number(phone):
    pattern = r'^(?:8|\+7)\d{10}$'
    cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
    return bool(re.match(pattern, cleaned_phone))


# Проверка на отсутствие состояний
class NoStates(Filter):
    async def __call__(self, message: Message, state: FSMContext):
        stat = await state.get_state()
        return stat == None


# Сообщение без состояний
@dp.message(NoStates())
async def no_states_handler(msg: Message, state: FSMContext):
    pass
        

# Сообщение от бизнес-бота
@dp.business_message()
async def business_handler(msg: Message, state: FSMContext):
    pass
