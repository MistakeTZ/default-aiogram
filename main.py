import asyncio
import logging
import sys
from database.model import DB


# Запуск бота
async def main() -> None:

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    raise KeyboardInterrupt


# Одновременное выполнение нескольких асинхронных функций
async def multiple_tasks():

    input_coroutines = [main(), repetition.send_messages()]
    res = await asyncio.gather(*input_coroutines)
    return res


# Запуск и остановка бота
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Загрузка всех файлов и модулей
    from loader import dp, bot

    # Загрузка обработчика команд
    from utils import repetition

    try:
        loop.run_until_complete(multiple_tasks())
    except KeyboardInterrupt:
        pass
    logging.info("Exiting")

    DB.unload_database()
