from os import environ, path, getenv
import json

config_file = {}


# Загрузка файла окружения
def load_env():
    with open('.env', 'r') as fh:
        vars_dict = dict(
            tuple(line.replace('\n', '').split('='))
            for line in fh.readlines() if not line.startswith('#')
        )

    environ.update(vars_dict)


# Получение текста из файла окружения по ключу
def get_env(key):
    return getenv(key)


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
