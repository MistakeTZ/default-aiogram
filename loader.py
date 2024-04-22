from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config import get_env, load_env
# from database.models import load
from support import messages

# Загрузка сообщений
messages.load_messages()

# Загрузка файлов окружения
load_env()
# Загрузка базы данных 
# load(False)


# Создание бота
bot = Bot(get_env("token"), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
