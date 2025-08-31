from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from tasks.config import get_env, load_env, load_config
from support.messages import MessageSender, JSONMessageSender
from database.model import init_db


# Загрузка файла окружения и файла конфигурации
load_env()
load_config()

# Загрузка базы данных и создание таблиц, если их не существует
init_db()

# Создание бота
bot = Bot(get_env("token"), default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

sender: MessageSender = JSONMessageSender(bot)

# Загрузка сообщений
sender.load_messages()
