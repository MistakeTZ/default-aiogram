from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from config import get_config, get_env
from loader import sender


# Inline клавиатура с n количеством кнопок
# Вызывается buttons(Текст 1-ой кнопки, Дата 1-ой кнопки, Текст 2-ой кнопки...)
def buttons(*args) -> InlineKeyboardMarkup:
    in_buttons = [[InlineKeyboardButton(
        text=sender.get_text(args[i * 2]),
        callback_data=args[i * 2 + 1] if len(args) >= (i + 1) * 2
        else args[i * 2])] for i in range((len(args) + 1) // 2)]
    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Reply клавиатура с одной кнопкой
def reply(name) -> ReplyKeyboardMarkup:
    in_buttons = [[KeyboardButton(text=sender.text(name))]]
    return ReplyKeyboardMarkup(keyboard=in_buttons,
                               one_time_keyboard=True, resize_keyboard=True)


# Таблица inline кнопок
def table(width: int, *args) -> InlineKeyboardMarkup:
    in_buttons = []
    index = 0

    while len(args) > index:
        in_buttons.append([])

        for _ in range(width):
            in_buttons[-1].append(
                InlineKeyboardButton(text=args[index],
                                     callback_data=args[index+1]))
            index += 2
            if len(args) == index:
                break

    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Таблица reply кнопок
def reply_table(width: int, one_time: bool = True, *args
                ) -> ReplyKeyboardMarkup:
    in_buttons = []
    index = 0

    while len(args) > index:
        in_buttons.append([])

        for _ in range(width):
            in_buttons[-1].append(KeyboardButton(text=args[index]))
            index += 1
            if len(args) == index:
                break

    return ReplyKeyboardMarkup(
        keyboard=in_buttons, one_time_keyboard=one_time, resize_keyboard=True)


# Клавиатура телефона
def phone() -> ReplyKeyboardMarkup:
    in_buttons = [[KeyboardButton(
        text=sender.text("send_contact"), request_contact=True)]]
    return ReplyKeyboardMarkup(keyboard=in_buttons,
                               one_time_keyboard=True, resize_keyboard=True)
