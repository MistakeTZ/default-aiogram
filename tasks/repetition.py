import asyncio
from tasks import kb
from tasks.loader import bot, sender, Repetition, User, session
from sqlalchemy import select, update
from .config import tz
from datetime import datetime
import handlers # Important


# Отправка запланированных сообщений
async def send_messages():
    await asyncio.sleep(5)

    while True:
        stmt = (
            select(Repetition)
            .where(Repetition.confirmed.is_(True))
            .where(Repetition.is_send.is_(False))
            .where(Repetition.time_to_send < datetime.now(tz=tz))
        )
        result = session.execute(stmt)
        messages_to_send = result.scalars().all()

        if messages_to_send:
            to_send_tasks = [send_msg(session, msg) for msg in messages_to_send]
            await asyncio.gather(*to_send_tasks)

        await asyncio.sleep(60)


async def send_msg(session, message: Repetition):
    # mark as sent
    session.execute(
        update(Repetition)
        .where(Repetition.chat_id == message.chat_id)
        .where(Repetition.message_id == message.message_id)
        .values(is_send=True)
    )
    session.commit()

    # fetch all users
    result = session.execute(select(User))
    all_users = result.scalars().all()

    # build reply
    if message.button_text and message.button_link:
        reply = kb.link(message.button_text, message.button_link)
    else:
        reply = None

    for user in all_users:
        try:
            await bot.copy_message(
                user.telegram_id,
                message.chat_id,
                message.message_id,
                reply_markup=reply,
            )
        except Exception:
            continue
