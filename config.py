import os
import json

config_file = {}

# Загрузка файла окружения
def load_env():
    with open('.env', 'r') as fh:
        vars_dict = dict(
            tuple(line.replace('\n', '').split('='))
            for line in fh.readlines() if not line.startswith('#')
        )

    os.environ.update(vars_dict)

    update_config()

# Получение текста из файла окружения по ключу
def get_env(key):
    return os.getenv(key)

# Чтение из файла конфигурации
def get_config(*args, **kwards):
    if not "config" in kwards:
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
        
# Обновление файла конфигурации
def update_config():
    global config_file
    with open(os.path.join("support", "config.json"), encoding='utf-8') as file:
        config_file = json.load(file)
