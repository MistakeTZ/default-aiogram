import asyncio
import logging
import sys


# Запуск бота
async def main() -> None:
    from tasks.config import set_bot_commands

    await set_bot_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

    raise KeyboardInterrupt


# Одновременное выполнение нескольких асинхронных функций
async def multiple_tasks():
    # Загрузка обработчика команд
    from tasks import repetition

    input_coroutines = [main(), repetition.send_messages()]
    res = await asyncio.gather(*input_coroutines)
    return res


# Запуск и остановка бота
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Загрузка всех файлов и модулей
    from tasks.loader import bot, dp

    try:
        loop.run_until_complete(multiple_tasks())
    except KeyboardInterrupt:
        pass
    logging.info("Exiting")
