import asyncio
from utils import kb
from loader import bot, sender
from config import time_difference
from database.model import DB
from datetime import datetime


# Отправка запланированных сообщений
async def send_messages():
    await asyncio.sleep(5)
    while True:
        messages_to_send = DB.get("select chat_id, message_id, \
            button_text, button_link, time_to_send from repetitions \
                where confirmed and not is_send and time_to_send < ?",
                [datetime.now() + time_difference])
        if messages_to_send:
            to_send_tasks = [send_msg(*msg) for msg in messages_to_send]
            await asyncio.gather(*to_send_tasks)

        await asyncio.sleep(60)


async def send_msg(chat_id, message_id, button_text, button_link, time_to_send):
    DB.commit("update repetitions set is_send = ? where chat_id = ? and message_id = ?", [True, chat_id, message_id])
    users = DB.get("select telegram_id from users")
    for user in users:
        try:
            if button_link:
                await bot.copy_message(user[0], chat_id, message_id, reply_markup=kb.link(button_text, button_link))
            else:
                await bot.copy_message(user[0], chat_id, message_id)
        except:
            continue
