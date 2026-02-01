from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tasks import kb
from tasks.loader import dp, sender


# Проверка на отсутствие состояний
class NoStates(Filter):
    async def __call__(self, msg: Message, state: FSMContext):
        stat = await state.get_state()
        return stat is None


# Сообщение без состояний
@dp.message(NoStates())
async def no_states_handler(msg: Message, state: FSMContext):
    pass
