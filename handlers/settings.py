from aiogram import F
from aiogram import types

from loader import db
from router import router
from localization.i18n import action_title
from keyboards.reply.settings_menu import generate_settings_menu
from constants import LastVisitedPlaces


@router.message(lambda message: message.text in ["⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"])
async def settings(message: types.Message):
    lang = db.get_user_lang(message.from_user.id)
    db.update_last_visited_place(LastVisitedPlaces.SETTINGS,
                                 message.from_user.id)
    await message.answer(text=f"{action_title.get(lang)}", reply_markup=generate_settings_menu(lang))
