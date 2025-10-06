from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from tasks.config import load_env, load_config
from support.messages import MessageSender, JSONMessageSender
from database.model import init_db


# Загрузка файла окружения и файла конфигурации
load_env()
load_config()
from tasks.config import settings # noqa F402

# Загрузка базы данных и создание таблиц, если их не существует
session = init_db()

# Создание бота
bot = Bot(settings.token, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

sender: MessageSender = JSONMessageSender(bot)

# Загрузка сообщений
sender.load_messages()
