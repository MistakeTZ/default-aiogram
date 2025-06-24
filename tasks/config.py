from aiogram.types import BotCommand
from os import path, getenv
import logging
import json
from datetime import timedelta, timezone
from dotenv import load_dotenv

config_file = {}
tz: timezone


# Загрузка файла окружения
def load_env():
    try:
        load_dotenv()
        set_time_difference()
    except Exception as e:
        logging.error("Loading failed")
        logging.error(e)


# Получение текста из файла окружения по ключу
def get_env(key):
    return getenv(key)


# Установка временного сдвига
def set_time_difference():
    global tz
    try:
        time_dif = int(get_env("time_difference"))
    except:
        time_dif = 0

    tz = timezone(timedelta(hours=time_dif))


# Чтение из файла конфигурации
def get_config(*args, **kwards):
    if "config" not in kwards:
        if args[0] in config_file:
            if len(args) == 1:
                return config_file[args[0]]
            return get_config(*args[1:], config=config_file[args[0]])
    else:
        if args[0] in kwards["config"]:
            if len(args) == 1:
                return kwards["config"][args[0]]
            return get_config(*args[1:], config=kwards["config"][args[0]])
    return False


# Загрузка файла конфигурации
def load_config():
    global config_file
    with open(path.join("support", "config.json"), encoding='utf-8') as file:
        config_file = json.load(file)


# Обновление файла конфигурации
def update_config(field, value):
    try:
        logging.info("Updating config variable '" + field + "' with value " + str(value))
        config_file[field] = value
        with open(path.join("support", "config.json"), "w", encoding='utf-8') as file:
            json.dump(config_file, file, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error("Updating failed")
        logging.error(e)


# Установка команд бота
async def set_bot_commands(bot):
    command_list = get_config("commands")
    commands = []
    for command in command_list:
        commands.append(BotCommand(command=command,
                                    description=command_list[command]))
    await bot.set_my_commands(commands)
