import abc
from aiogram import Bot
from aiogram.types import Message, FSInputFile
from os.path import join, exists


# Загрузчик сообщений
class MessageSender():

    # Все доступные сообщения
    messages = {}
    bot: Bot

    def __init__(self, bot) -> None:
        self.bot = bot

    @abc.abstractmethod
    def load_messages(self, path_to_file: str = None):
        """
        Метод загружает все сообщения из файла
        """
        return

    # Получение текста сообщения по ключу с указанием аргументов
    def text(self, key: str, *args) -> str:
        if key in self.messages:
            return self.messages[key].format(*args)
        
        print(f"Key {key} not found")
        return self.messages["default"]
    
    # Отправка сообщения пользователю
    async def message(self, chat_id: int, key: str, reply_markup = None, *args):
        text = self.text(key, *args)
        await self.bot.send_message(chat_id, text, reply_markup=reply_markup)

    # Изменение сообщения
    async def edit_message(self, msg: Message, key: str, reply_markup = None, *args):
        text = self.text(key, *args)
        await msg.edit_text(text, reply_markup=reply_markup)

    # Открытие медиа
    async def send_media(self, chat_id: int, media_type: str,
                         media: str, key: str = None, reply_markup = None,
                         path: str = None, name: str = None, *args):
        if key:
            text = self.text(key, *args)
        else:
            text = None
        
        if name:
            name = name + "." + media.split(".")[1]
        else:
            name = media

        if path:
            path = join(path, media)
        else:
            path = join("support", "media", media)

        file = FSInputFile(path=path, filename=name)

        match media_type:
            case "photo":
                await self.bot.send_photo(chat_id, file, caption=text,
                                          reply_markup=reply_markup)
            case "video":
                await self.bot.send_video(chat_id, file, caption=text,
                                          reply_markup=reply_markup)
            case "audio":
                await self.bot.send_audio(chat_id, file, caption=text,
                                          reply_markup=reply_markup)
            case "file":
                await self.bot.send_document(chat_id, file, caption=text,
                                             reply_markup=reply_markup)

# Загрузчик сообщений из JSON файла
class JSONMessageSender(MessageSender):

    # Загрузка всех сообщений
    def load_messages(self, path_to_file: str = None):
        import json

        # Файл не предопределен
        if not path_to_file:
            path_to_file = join("support", "messages.json")

        # Файл не найден
        if not exists(path_to_file):
            raise ValueError('Message file not found')

        # Загрузка сообщений
        with open(path_to_file, encoding='utf8') as file:
            self.messages = json.load(file)

        # Сообщение об успешной загрузке
        if "succeful_load" in self.messages:
            print(self.messages["succeful_load"])

        return True
