from datetime import datetime
from os import path

from aiogram import F
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hlink

from database.model import Repetition, User
from tasks import kb
from tasks.config import get_config, tz
from tasks.loader import bot, dp, sender, session
from tasks.states import UserState


class AdminFilter(Filter):
    async def __call__(self, message):
        user_id = message.from_user.id
        user = session.query(User).filter_by(telegram_id=user_id).one_or_none()
        if not user:
            await sender.message(user_id, "not_allowed")
            return False
        if user.role != "admin":
            await sender.message(user_id, "not_allowed")
            return False
        return True


# Панель администратора
@dp.message(Command("admin"), AdminFilter())
@dp.callback_query(F.data == "admin")
async def command_settings(
    data: Message | CallbackQuery,
    state: FSMContext,
) -> None:
    user_id = data.from_user.id
    reply = []
    for scope in get_config("admin_scope"):
        reply.extend(["admin_" + scope] * 2)
    reply.extend(["main_menu", "menu"])
    reply = kb.table(2, *reply, is_keys=True)

    if isinstance(data, Message):
        await sender.message(user_id, "admin_panel", reply)
    else:
        await sender.edit_message(data.message, "admin_panel", reply)


# Кнопка рассылки
@dp.callback_query(F.data == "admin_mail")
async def mailing_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    await sender.edit_message(clbck.message, "write_message_for_mailing")
    await state.set_state(UserState.mailing)
    await state.set_data({"status": "begin"})


# Кнопка получения БД
@dp.callback_query(F.data == "admin_db")
async def db_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    user_id = clbck.from_user.id
    await sender.send_media(
        user_id,
        "document",
        "db.sqlite3",
        path="database",
        name="db",
    )


# Кнопка списка пользователей
@dp.callback_query(F.data == "admin_list")
async def list_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    all_users = session.query(User).all()
    message = ""
    for user in all_users:
        message += hlink(user.name, f"tg://user?id={user.telegram_id}")
        if user.username:
            message += f" (@{user.username})"
        message += f" - {user.role}"
        message += "\n"

    await sender.edit_message(
        clbck.message,
        "users",
        kb.buttons(True, "admin"),
        message,
    )


# Изменение роли
@dp.callback_query(F.data.startswith("admin_role"))
async def role_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    data = clbck.data.split("_")
    if len(data) == 2:
        await sender.edit_message(
            clbck.message,
            "choose_role",
            kb.table(
                2,
                "new_admin",
                "admin_role_admin",
                "new_user",
                "admin_role_user",
                "admin",
                "admin",
                is_keys=True,
            ),
        )
        return
    elif len(data) == 3:
        await sender.edit_message(
            clbck.message,
            "choose_user",
            kb.user_table(clbck.data),
        )
    else:
        role = data[2]
        user = data[3]
        user_ = session.query(User).filter_by(id=user).one()
        user_.role = role
        session.commit()
        await sender.edit_message(
            clbck.message,
            "role_updated",
            kb.buttons(True, "admin"),
        )


# Бан пользователя
@dp.callback_query(F.data.startswith("admin_ban"))
async def ban_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    data = clbck.data.split("_")
    if len(data) == 2:
        is_ban = data[1] == "ban"
        await sender.edit_message(
            clbck.message,
            "choose_user",
            kb.user_table(clbck.data, not is_ban),
        )
    else:
        user = data[2]
        is_ban = data[1] == "ban"
        user_ = session.query(User).filter_by(id=user).one()
        user_.restricted = is_ban
        session.commit()
        await sender.edit_message(
            clbck.message,
            "user_banned" if is_ban else "user_unbanned",
            kb.buttons(True, "admin"),
        )


# Рассылка
@dp.message(UserState.mailing)
async def mailing(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()

    match data["status"]:
        case "begin":
            repetition = Repetition(
                chat_id=user_id,
                message_id=msg.message_id,
            )
            session.add(repetition)
            session.commit()
            zapis_id = (
                session.query(Repetition)
                .order_by(
                    Repetition.id.desc(),
                )
                .first()
                .id
            )

            await state.set_data({"status": "is_button", "id": zapis_id})
            await sender.message(
                user_id,
                "want_to_add_button",
                kb.reply_table(
                    2,
                    *sender.text("yes_not").split("/"),
                    is_keys=False,
                ),
            )

        case "is_button":
            is_true = sender.text("yes_not").split("/").index(msg.text) == 0
            if is_true:
                await state.set_data({"status": "link", "id": data["id"]})
                await sender.message(user_id, "write_button_link", kb.remove())
            else:
                await state.set_data(
                    {
                        "status": "time",
                        "id": data["id"],
                        "link": "",
                        "text": "",
                    },
                )
                await sender.message(
                    user_id,
                    "write_time",
                    kb.reply(
                        sender.text("now"),
                    ),
                )

        case "link":
            await state.set_data(
                {"status": "text", "id": data["id"], "link": msg.text},
            )
            await sender.message(user_id, "write_button_text")

        case "text":
            if len(msg.text) > 30:
                await sender.message(user_id, "wrong_text")
            else:
                await state.set_data(
                    {
                        "status": "time",
                        "id": data["id"],
                        "link": data["link"],
                        "text": msg.text,
                    },
                )
                await sender.message(
                    user_id,
                    "write_time",
                    kb.reply(sender.text("now")),
                )

        case "time":
            try:
                if msg.text == sender.text("now"):
                    date = datetime.now(tz=tz)
                else:
                    date = datetime.strptime(msg.text, "%d.%m.%Y %H:%M")
                rep = (
                    session.query(Repetition)
                    .filter_by(
                        id=data["id"],
                    )
                    .first()
                )
                rep.button_text = data["text"]
                rep.button_link = data["link"]
                rep.time_to_send = date
                session.commit()

                await sender.message(user_id, "message_to_send")

                message_id = rep.message_id
                await bot.copy_message(
                    user_id,
                    user_id,
                    message_id,
                    reply_markup=(
                        kb.link(
                            data["text"],
                            data["link"],
                        )
                        if data["link"]
                        else None
                    ),
                )
                await sender.message(
                    user_id,
                    "type_confirm",
                    kb.remove(),
                    sender.text("confirm"),
                )
                await state.set_data({"status": "confirm", "id": data["id"]})
            except Exception as e:
                print(e)
                await sender.message(user_id, "wrong_date")

        case "confirm":
            await state.set_state(UserState.default)
            if msg.text.lower() == sender.text("confirm").lower():
                await sender.message(user_id, "message_sended")
                rep = (
                    session.query(Repetition)
                    .filter_by(
                        id=data["id"],
                    )
                    .first()
                )
                rep.confirmed = True
                session.commit()
            else:
                await sender.message(user_id, "aborted")


# Установка базы данных
@dp.message(F.document, AdminFilter())
async def set_databse(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    user = session.query(User).filter_by(telegram_id=user_id).one()
    if not user:
        return
    if user.role != "admin":
        return

    doc = msg.document
    if doc.file_name.split(".")[-1] != "sqlite3":
        return

    db_file = await bot.get_file(doc.file_id)
    await bot.download_file(
        db_file.file_path,
        path.join("database", "db.sqlite3"),
    )
