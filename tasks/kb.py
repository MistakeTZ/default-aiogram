from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from tasks.loader import sender, session
from database.model import User


# Удаление клавиатуры
def remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()


# Inline клавиатура с n количеством кнопок
# Вызывается buttons(Текст 1-ой кнопки, Дата 1-ой кнопки, Текст 2-ой кнопки...)
def buttons(is_keys: bool, *args) -> InlineKeyboardMarkup:
    if is_keys:
        in_buttons = [
            [
                InlineKeyboardButton(
                    text=sender.text(args[i * 2]),
                    callback_data=args[i * 2 + 1] if len(args) >= (i + 1) * 2
                    else args[i * 2],
                ),
            ] for i in range((len(args) + 1) // 2)
        ]
    else:
        in_buttons = [
            [
                InlineKeyboardButton(
                    text=args[i * 2],
                    callback_data=args[i * 2 + 1] if len(args) >= (i + 1) * 2
                    else args[i * 2],
                ),
            ] for i in range((len(args) + 1) // 2)
        ]
    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Reply клавиатура с одной кнопкой
def reply(name) -> ReplyKeyboardMarkup:
    in_buttons = [[KeyboardButton(text=name)]]
    return ReplyKeyboardMarkup(
        keyboard=in_buttons,
        one_time_keyboard=True,
        resize_keyboard=True,
    )


# Таблица inline кнопок
def table(width: int, *args, **kwards) -> InlineKeyboardMarkup:
    in_buttons = []
    index = 0
    is_keys = kwards.get("is_keys", False)

    while len(args) > index:
        in_buttons.append([])

        for _ in range(width):
            in_buttons[-1].append(
                InlineKeyboardButton(
                    text=sender.text(
                        args[index],
                    ) if is_keys else args[index],
                    callback_data=args[index + 1],
                ),
            )
            index += 2
            if len(args) == index:
                break

    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Таблица reply кнопок
def reply_table(
        width: int,
        *args,
        **kwards,
) -> ReplyKeyboardMarkup:
    one_time = kwards.get("one_time", True)

    is_keys = kwards.get("is_keys", False)

    in_buttons = []
    index = 0

    while len(args) > index:
        in_buttons.append([])

        for _ in range(width):
            if is_keys:
                in_buttons[-1].append(
                    KeyboardButton(text=sender.text(args[index])),
                )
            else:
                in_buttons[-1].append(KeyboardButton(text=args[index]))
            index += 1
            if len(args) == index:
                break

    return ReplyKeyboardMarkup(
        keyboard=in_buttons, one_time_keyboard=one_time, resize_keyboard=True)


# Клавиатура телефона
def phone() -> ReplyKeyboardMarkup:
    in_buttons = [
        [
            KeyboardButton(
                text=sender.text("send_contact"),
                request_contact=True,
            ),
        ],
    ]
    return ReplyKeyboardMarkup(
        keyboard=in_buttons,
        one_time_keyboard=True,
        resize_keyboard=True,
    )


# Кнопки ссылки
def link(text, url) -> InlineKeyboardMarkup:
    in_buttons = [[InlineKeyboardButton(text=text, url=url)]]
    return InlineKeyboardMarkup(inline_keyboard=in_buttons)


# Таблица пользователей
def user_table(data, restrict=False):
    all_users = session.query(User).filter_by(restricted=restrict).all()
    buttons = []

    for i, user in enumerate(all_users):
        if i % 2 == 0:
            buttons.append([])

        name = user.name
        if user.username:
            name += f" (@{user.username})"

        buttons[-1].append(InlineKeyboardButton(
            text=name,
            callback_data=f"{data}_{user.id}",
        ))
    buttons.append([
        InlineKeyboardButton(
            text=sender.text("admin"),
            callback_data="admin",
        ),
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
