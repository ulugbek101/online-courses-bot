from aiogram.types import ContentType, Message
from router import router


@router.message()
async def vide_id(message: Message):
    print('Message', message.document.file_id)

