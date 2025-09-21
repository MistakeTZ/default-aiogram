import asyncio

from aiogram import F
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.utils.markdown import hlink
from aiogram.fsm.context import FSMContext

import tasks.kb as kb
from tasks.loader import dp, bot, sender, session, User
from tasks.states import UserState


# Установка электронной почты
@dp.message(UserState.email)
async def email_check(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if not msg.entities:
        await sender.message(user_id, "wrong_email")
        return
    email_entity = msg.entities[0]
    if email_entity.type != "email":
        await sender.message(user_id, "wrong_email")
        return
    email = msg.text[email_entity.offset:email_entity.length]


# Установка телефона
@dp.message(UserState.phone, F.contact)
async def phone_check(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    phone = msg.contact.phone_number


# Проверка на отсутствие состояний
class NoStates(Filter):
    async def __call__(self, msg: Message, state: FSMContext):
        stat = await state.get_state()
        return stat is None


# Сообщение без состояний
@dp.message(NoStates())
async def no_states_handler(msg: Message, state: FSMContext):
    pass
