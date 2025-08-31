from aiogram import F
from aiogram.filters import Filter, Command
from database.model import users
from tasks.loader import sender, dp
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.utils.markdown import hlink
from tasks.states import UserState
from tasks.config import get_config
from tasks import kb


class AdminFilter(Filter):
    async def __call__(self, message):
        user_id = message.from_user.id
        user = users.filter(telegram_id=user_id).one()
        if not user:
            await sender.message(user_id, "not_allowed")
            return False
        if user["role"] != "admin":
            await sender.message(user_id, "not_allowed")
            return False
        return True


# Панель администратора
@dp.message(Command("admin"), AdminFilter())
@dp.callback_query(F.data == "admin")
async def command_settings(data: Message | CallbackQuery, state: FSMContext) -> None:
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
async def mailing_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    user_id = clbck.from_user.id
    await sender.send_media(user_id, "file", "db.sqlite3", path="database", name="db")


# Кнопка списка пользователей
@dp.callback_query(F.data == "admin_list")
async def mailing_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    all_users = users.all()
    message = ""
    for user in all_users:
        message += hlink(user["name"], f"tg://user?id={user['telegram_id']}")
        if user["username"]:
            message += f" (@{user['username']})"
        message += f" - {user['role']}"
        message += "\n"
    
    await sender.edit_message(clbck.message, "users", kb.buttons(True, "admin"), message)


# Изменение роли
@dp.callback_query(F.data.startswith("admin_role"))
async def role_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    user_id = clbck.from_user.id
    data = clbck.data.split("_")
    if len(data) == 2:
        await sender.edit_message(clbck.message, "choose_role", kb.table(2,
            "new_admin", "admin_role_admin", "new_user", "admin_role_user",
            "admin", "admin", is_keys=True))
        return
    elif len(data) == 3:
        await sender.edit_message(clbck.message, "choose_user", kb.user_table(clbck.data))
    else:
        role = data[2]
        user = data[3]
        users.filter(id=user).update(role=role)
        await sender.edit_message(clbck.message, f"role_updated", kb.buttons(True, "admin"))


# Бан пользователя
@dp.callback_query(F.data.startswith("admin_ban"))
async def ban_handler(clbck: CallbackQuery, state: FSMContext) -> None:
    data = clbck.data.split("_")
    if len(data) == 2:
        is_ban = data[1] == "ban"
        await sender.edit_message(clbck.message, "choose_user",
                        kb.user_table(clbck.data, not is_ban))
    else:
        user = data[2]
        is_ban = data[1] == "ban"
        users.filter(id=user).update(restricted=is_ban)
        await sender.edit_message(clbck.message, f"user_banned" if is_ban
                            else "user_unbanned", kb.buttons(True, "admin"))
