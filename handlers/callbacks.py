from aiogram import F
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from tasks.loader import dp, bot, sender

from tasks import kb
from tasks.states import UserState


# Возвращение в меню
@dp.callback_query(F.data == "back")
async def menu_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    user_id = clbck.from_user.id
    await sender.edit_message(clbck.message, "menu")
    await state.set_state(UserState.default)


# Начинается с
@dp.callback_query(F.data.startswith("start_"))
async def start_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    user_id = clbck.from_user.id
    answer = clbck.data.split("_")[-1]
