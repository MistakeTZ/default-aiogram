from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from support.messages import get_text
from datetime import datetime
from config import get_config, get_env, update_config


# Inline клавиатура с n количеством кнопок
# Вызывается, как buttons(Текст первой кнопки, Дата первой кнопки, Текст второй кнопки...)
def buttons(*args) -> InlineKeyboardMarkup:
    in_buttons = [[InlineKeyboardButton(text=get_text(args[i * 2]), callback_data=args[i * 2 + 1] if len(args) >= (i + 1) * 2 else args[i * 2])]
               for i in range((len(args) + 1) // 2)]
    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Inline клавиатура с 2 кнопками в 1 ряд
def two_buttons(name1: str, data1: str, name2: str, data2: str) -> InlineKeyboardMarkup:
    in_buttons = [[InlineKeyboardButton(text=name1, callback_data=data1),
               InlineKeyboardButton(text=name2, callback_data=data2)]]
    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Reply клавиатура с одной кнопкой
def reply(name) -> ReplyKeyboardMarkup:
    in_buttons = [[KeyboardButton(text=get_text(name))]]
    return ReplyKeyboardMarkup(keyboard=in_buttons, one_time_keyboard=True, resize_keyboard=True)


# Таблица inline кнопок
def table(width: int, height: int, *args) -> InlineKeyboardMarkup:
    in_buttons = []
    index = 0

    for y in range(height):
        in_buttons.append([])

        for x in range(width):
            in_buttons[y].append(InlineKeyboardButton(text=args[index], callback_data=args[index+1]))
            index += 2

    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Таблица reply кнопок
def reply_table(width: int, height: int, one_time: bool = True, *args) -> ReplyKeyboardMarkup:
    in_buttons = []
    index = 0

    for y in range(height):
        in_buttons.append([])

        for x in range(width):
            in_buttons[y].append(KeyboardButton(text=args[index]))
            index += 1

    return ReplyKeyboardMarkup(keyboard=in_buttons, one_time_keyboard=one_time, resize_keyboard=True)


# Клавиатура телефона
def phone() -> ReplyKeyboardMarkup:
    in_buttons = [[KeyboardButton(text=get_text("send_contact"))]]
    return ReplyKeyboardMarkup(keyboard=in_buttons, one_time_keyboard=True, resize_keyboard=True)
