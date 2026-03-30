from maxapi.filters import BaseFilter
from maxapi.context import MemoryContext
from maxapi.types import MessageCreated
from maxapi.enums.attachment import AttachmentType

from tasks import kb
from tasks.loader import dp, sender


# Проверка на отсутствие состояний
class PhotoFilter(BaseFilter):
    async def __call__(self, event):
        if not isinstance(event, MessageCreated):
            return False
        return (
            event.message.body.attachments
            and event.message.body.attachments[0].type == AttachmentType.PHOTO
        )


# Сообщение без состояний
@dp.message_created(PhotoFilter())
async def photo_handler(event: MessageCreated, context: MemoryContext): ...
