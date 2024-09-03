from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import get_env, load_env
from support.messages import *


# Загрузка файлов окружения
load_env()

# Создание бота
bot = Bot(get_env("token"), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

sender: MessageSender = JSONMessageSender(bot)

# Загрузка сообщений
sender.load_messages()
