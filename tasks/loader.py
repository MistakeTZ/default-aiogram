from maxapi import Bot, Dispatcher
from maxapi.enums.parse_mode import ParseMode

from database.model import init_db
from support.messages import JSONMessageSender, MessageSender
from tasks.config import load_config, load_env

# Загрузка файла окружения и файла конфигурации
load_env()
load_config()
from tasks.config import settings  # noqa F402

# Загрузка базы данных и создание таблиц, если их не существует
session = init_db()

# Создание бота
bot = Bot(settings.TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

sender: MessageSender = JSONMessageSender(bot)

# Загрузка сообщений
sender.load_messages()
