from maxapi.types import CallbackButton, MessageButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from tasks.loader import sender


# Inline клавиатура с n количеством кнопок
def buttons(is_keys: bool, is_callback: bool, buttons) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for button in buttons:
        if is_callback:
            builder.add(
                CallbackButton(
                    text=sender.text(button[0]) if is_keys else button[0],
                    callback_data=button[1],
                )
            )
        else:
            builder.add(
                MessageButton(
                    text=sender.text(button) if is_keys else button,
                )
            )

    return builder.as_markup()


# Reply клавиатура с одной кнопкой
def reply(name) -> InlineKeyboardBuilder:
    markup = InlineKeyboardBuilder()
    markup.add(MessageButton(text=name))
    return markup.as_markup()


# Кнопки ссылки
def link(text, url) -> InlineKeyboardBuilder:
    markup = InlineKeyboardBuilder()
    markup.add(
        LinkButton(
            text=text,
            url=url,
        )
    )
    return markup.as_markup()
