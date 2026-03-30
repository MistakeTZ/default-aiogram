import asyncio
import logging
from datetime import datetime

from sqlalchemy import update

import handlers  # noqa F401
from database.model import Repetition, User
from tasks import kb
from tasks.loader import bot, session

from .config import tz


# Отправка запланированных сообщений
async def send_messages():
    await asyncio.sleep(5)

    while True:
        messages_to_send = (
            session.query(Repetition)
            .filter(
                Repetition.confirmed == True,
                Repetition.is_send == False,
                Repetition.time_to_send < datetime.now(tz=tz),
            )
            .all()
        )

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
        .values(is_send=True),
    )
    session.commit()

    # fetch all users
    all_users = session.query(User).filter_by(enabled_rep=True).all()

    # build reply
    if message.button_text and message.button_link:
        reply = kb.link(message.button_text, message.button_link)
    else:
        reply = None

    for i, user in enumerate(all_users):
        await asyncio.sleep(0.25)
        if i % 2300 == 2299:
            await asyncio.sleep(60 * 60)
        try:
            await bot.send_message(
                chat_id=user.chat_id,
                text=message.text,
                attachments=[reply] if reply else None,
            )
        except Exception as e:
            logging.warning(
                f"Failed to send message to {user.chat_id}: {e}",
            )
