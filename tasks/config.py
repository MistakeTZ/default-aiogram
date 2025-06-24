from os import environ, path, getenv
import logging
import json
from datetime import timedelta

config_file = {}
time_difference: timedelta


# Загрузка файла окружения
def load_env():
    try:
        logging.info("Loading environment variables")
        with open('.env', 'r') as fh:
            vars_dict = dict(
                tuple(line.replace('\n', '').split('='))
                for line in fh.readlines() if not line.startswith('#')
            )

        environ.update(vars_dict)

        set_time_difference()
    except Exception as e:
        logging.error("Loading failed")
        logging.error(e)


# Получение текста из файла окружения по ключу
def get_env(key):
    return getenv(key)


# Установка временного сдвига
def set_time_difference():
    global time_difference
    try:
        time_dif = int(get_env("time_difference"))
    except:
        time_dif = 0

    time_difference = timedelta(hours=time_dif)


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
