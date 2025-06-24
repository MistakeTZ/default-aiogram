from aiogram.fsm.state import State, StatesGroup


# Файл состояний FSM
class UserState(StatesGroup):
    default = State()
    admin = State()
    email = State()
    phone = State()
    time = State()
    mailing = State()
