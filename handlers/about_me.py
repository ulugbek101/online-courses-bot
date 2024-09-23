from typing import AsyncGenerator
from aiogram import Bot, types
from aiogram.types import InputFile

from router import router
from loader import db, bot
from localization.i18n import about_me_text


@router.message(lambda message: message.text in ["ℹ️ Men haqimda", "ℹ️ Обо мне", "ℹ️ About me"])
async def about_me(message: types.Message):
    lang = db.get_user_lang(message.from_user.id)

    photo = types.FSInputFile("media/about_me.jpg")

    await message.answer_photo(
        photo=photo,
        caption=f"{about_me_text.get(lang)}",
    )
