import logging

from maxapi.types import BotStarted, CommandStart
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from maxapi.types.users import User as MaxUser

from database.model import User
from tasks.config import get_config
from tasks.loader import dp, sender, session


@dp.message_created(CommandStart())
async def command_start_handler(event: MessageCreated, context: MemoryContext) -> None:
    await start_bot(event.chat.chat_id, event.from_user, context)


@dp.bot_started()
async def on_startup(event: BotStarted, context: MemoryContext) -> None:
    await start_bot(event.chat_id, event.user, context)


async def start_bot(chat_id, max_user: MaxUser, context: MemoryContext) -> None:
    user = session.query(User).filter_by(chat_id=chat_id).one_or_none()

    if not user:
        user_id = max_user.user_id
        logging.info(f"New user: {user_id}")
        user = User(
            user_id=user_id,
            chat_id=chat_id,
            name=max_user.full_name,
            username=max_user.username,
        )
        if user_id in get_config("admins"):
            user.role = "admin"
        session.add(user)
        session.commit()

    await sender.message(user_id, "start")
    await context.clear()
