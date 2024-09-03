import abc
from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.types.callback_query import CallbackQuery
from os import path


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
    def get_text(self, key: str, *args) -> str:
        if key in self.messages:
            return self.messages[key].format(*args)
        
        print(f"Key {key} not found")
        return self.messages["default"]
    

    # Отправка сообщения пользователю
    async def send_message(self, chat_id: int, key: str, reply_markup = None, *args):
        text = self.get_text(key, *args)
        await self.bot.send_message(chat_id, text, reply_markup=reply_markup)


    # Изменение сообщения
    async def edit_message(self, msg: Message, key: str, reply_markup = None, *args):
        text = self.get_text(key, *args)
        await msg.edit_text(text, reply_markup=reply_markup)


    # Отправка медиа пользователю
    async def send_media(self, chat_id: int, key: str = None, reply_markup = None, *args, **kwargs):
        # Добавление текста
        if key:
            text = self.get_text(key, *args)
        else:
            text = None

        # Отправка фото
        if "photo" in kwargs:
            photo_name = kwargs["photo_name"] if "photo_name" in kwargs else "photo"
            photo = FSInputFile(path=kwargs["photo"], filename=photo_name)

            await self.bot.send_photo(chat_id, photo, caption=text, reply_markup=reply_markup)

        # Отправка аудио
        if "audio" in kwargs:
            audio_name = kwargs["audio_name"] if "audio_name" in kwargs else "audio"
            audio = FSInputFile(path=kwargs["audio"], filename=audio_name)

            await self.bot.send_audio(chat_id, audio, caption=text, reply_markup=reply_markup)

        # Отправка видео
        if "video" in kwargs:
            video_name = kwargs["video_name"] if "video_name" in kwargs else "video"
            video = FSInputFile(path=kwargs["video"], filename=video_name)

            await self.bot.send_video(chat_id, video, caption=text, reply_markup=reply_markup)


# Загрузчик сообщений из CSV файла
class JSONMessageSender(MessageSender):

    # Загрузка всех сообщений
    def load_messages(self, path_to_file: str = None):
        import csv

        # Файл не предопределен
        if not path_to_file:
            path_to_file = path.join("support", "messages.csv")

        # Файл не найден
        if not path.exists(path_to_file):
            raise ValueError('Message file not found')

        # Загрузка сообщений
        with open(path_to_file, encoding='utf8') as file:
            reader = csv.reader(file)

            for message_pair in reader:
                self.messages[message_pair[0]] = message_pair[1]

        # Сообщение об успешной загрузке
        if "succeful_load" in self.messages:
            print(self.messages["succeful_load"])

        return True
    

    # Получение текста сообщения по ключу с указанием аргументов
    def get_text(self, key: str, *args) -> str:
        if key in self.messages:
            return self.messages[key].replace("\\n", "\n").replace("\"\"", "\"").format(*args)
        
        print(f"Key {key} not found")
        return self.messages["default"]


# Загрузчик сообщений из JSON файла
class JSONMessageSender(MessageSender):

    # Загрузка всех сообщений
    def load_messages(self, path_to_file: str = None):
        import json

        # Файл не предопределен
        if not path_to_file:
            path_to_file = path.join("support", "messages.json")

        # Файл не найден
        if not path.exists(path_to_file):
            raise ValueError('Message file not found')

        # Загрузка сообщений
        with open(path_to_file, encoding='utf8') as file:
            self.messages = json.load(file)

        # Сообщение об успешной загрузке
        if "succeful_load" in self.messages:
            print(self.messages["succeful_load"])

        return True
