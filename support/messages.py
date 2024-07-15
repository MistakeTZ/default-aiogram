import csv
from aiogram.types import Message, FSInputFile
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext
from states import UserState
from os import path

messages = {}

# Загрузка всех сообщений
def load_messages():
    global messages
    with open(path.join("support", "messages.csv"), encoding='utf8') as f:
        reader = csv.reader(f)
        for line in reader:
            messages[line[0]] = line[1]

    if "succeful_load" in messages.keys():
        print(messages["succeful_load"])


# Получение текста сообщения по ключу
def get_text(key: str, *args) -> str:
    if key in messages.keys():
        return messages[key].replace("\\n", "\n").replace("\"\"", "\"").format(*args)
    return messages["default"]


# Отправка сообщения пользователю
async def message(msg: Message, key: str, reply_markup=None, *args):
    text = get_text(key, *args)
    await msg.answer(text, reply_markup=reply_markup)


# Отправка сообщения, клавиатуры и изменение состояния
async def send_message(msg: Message | CallbackQuery, text: str = None, reply_markup = None, state: FSMContext = None, new_state: UserState = None, *args, **kwargs):
    if isinstance(msg, CallbackQuery):
        msg = msg.message
        await msg.edit_reply_markup()
        
    if state != None:
        await state.set_state(new_state)

    if "photo" in kwargs.keys():
        photo = FSInputFile(path=kwargs["photo"])
        await msg.answer_photo(photo)

    if "audio" in kwargs.keys():
        photo = FSInputFile(path=kwargs["audio"])
        await msg.answer_audio(photo)

    if text:
        await message(msg, text, reply_markup, *args)
