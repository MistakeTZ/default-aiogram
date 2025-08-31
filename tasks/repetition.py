import asyncio
from tasks import kb
from tasks.loader import bot, sender
from .config import tz
from database.model import repetitions, users
from datetime import datetime
import handlers # Important


# Отправка запланированных сообщений
async def send_messages():
    await asyncio.sleep(5)
    while True:
        messages_to_send = repetitions.filter(confirmed=True, is_send=False, time_to_send__lt=datetime.now(tz=tz)).all()

        if messages_to_send:
            to_send_tasks = [send_msg(msg) for msg in messages_to_send]
            await asyncio.gather(*to_send_tasks)

        await asyncio.sleep(60)


async def send_msg(message):
    repetitions.filter(chat_id=message["chat_id"], message_id=message["message_id"]).update(is_send=True)
    all_users = users.all()

    if message["button_text"] and message["button_link"]:
        reply = kb.link(message["button_text"], message["button_link"])
    else:
        reply = None

    for user in all_users:
        try:
            await bot.copy_message(user["telegram_id"], message["chat_id"], message["message_id"], reply_markup=reply)
        except:
            continue
