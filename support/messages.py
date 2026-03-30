import abc
from os.path import exists, join
import logging

from maxapi import Bot
from maxapi.types import InputMedia, Message
from maxapi.enums.upload_type import UploadType

logger = logging.getLogger(__name__)


# Загрузчик сообщений
class MessageSender:

    # Все доступные сообщения
    messages = {}
    bot: Bot

    def __init__(self, bot) -> None:
        """Определение бота."""
        self.bot = bot

    @abc.abstractmethod
    def load_messages(self, path_to_file: str = None):
        """Метод загружает все сообщения из файла."""
        return

    # Получение текста сообщения по ключу с указанием аргументов
    def part_text(self, key: str, messages: dict):
        parts = key.split(".")
        if parts[0] in messages:
            if "." in key:
                return self.part_text(
                    key[key.find(".") + 1 :],
                    messages[parts[0]],
                )
            return messages[key]

    # Получение текста сообщения по ключу с указанием аргументов
    def text(self, key: str, *args) -> str:
        text = self.part_text(key, self.messages)
        if text:
            return text.format(*args)

        logger.warning(f"Key {key} not found")
        return self.messages["default"]

    # Отправка сообщения пользователю
    async def message(
        self,
        chat_id: int,
        key: str,
        reply=None,
        *args,
        **kwargs,
    ):
        attachments = kwargs.pop("attachments", [])
        if reply:
            attachments.append(reply)

        text = self.text(key, *args)
        await self.bot.send_message(
            chat_id,
            text=text,
            attachments=attachments or None,
            **kwargs,
        )

    # Изменение сообщения
    async def edit_message(
        self,
        mid: str,
        key: str,
        reply=None,
        *args,
    ):
        text = self.text(key, *args)
        await self.bot.edit_message(
            mid, text=text, attachments=[reply] if reply else None
        )

    # Отправление кешированного медиа
    async def send_cached_media(
        self,
        chat_id: int,
        media_type: str,
        media: str,
        key: str = None,
        reply=None,
        *args,
    ):
        if key:
            text = self.text(key, *args)
        else:
            text = None

        kwargs = {
            "chat_id": chat_id,
            media_type: media,
            "caption": text,
            "reply_markup": reply,
        }

        coroutine = getattr(self.bot, "send_" + media_type)
        await coroutine(**kwargs)

    # Открытие медиа
    async def send_media(
        self,
        chat_id: int,
        media_type: str,
        media: str,
        key: str = None,
        reply=None,
        path: str = None,
        name: str = None,
        *args,
    ):
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

        media_file = InputMedia(path, UploadType.FILE)

        await self.message(
            chat_id,
            key or "null",
            reply,
            attachments=[media_file],
        )


# Загрузчик сообщений из JSON файла
class JSONMessageSender(MessageSender):
    def load_messages(self, path_to_file: str = None):
        import json

        # Файл не предопределен
        if not path_to_file:
            path_to_file = join("support", "messages.json")

        # Файл не найден
        if not exists(path_to_file):
            raise ValueError("Message file not found")

        # Загрузка сообщений
        with open(path_to_file, encoding="utf8") as file:
            self.messages = json.load(file)

        # Сообщение об успешной загрузке
        if "succeful_load" in self.messages:
            print(self.messages["succeful_load"])

        return True
