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


# Inline клавиатура настроек
def settings() -> InlineKeyboardMarkup:
    in_buttons = [
               [InlineKeyboardButton(text=get_text("back"), callback_data="back")]]
    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Reply клавиатура
def reply(name) -> ReplyKeyboardMarkup:
    in_buttons = [[KeyboardButton(text=get_text(name))]]
    return ReplyKeyboardMarkup(keyboard=in_buttons, one_time_keyboard=True, resize_keyboard=True)


# Кнопки городов
def cities() -> InlineKeyboardMarkup:
    cities = get_config("cities")
    buttons = []
    for city in cities:
        buttons.append([InlineKeyboardButton(text=cities[city]["name"], callback_data="choose_city_" + city)])
    
    buttons.append([InlineKeyboardButton(text=get_text("other_city"), callback_data="choose_city_other")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
