from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import get_env, load_env, load_config
from support.messages import *


# Загрузка файла окружения и файла конфигурации
load_env()
load_config()

# Создание бота
bot = Bot(get_env("token"), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

sender: MessageSender = JSONMessageSender(bot)

# Загрузка сообщений
sender.load_messages()
