from aiogram import types
from aiogram.fsm.context import FSMContext

from loader import db
from localization.i18n import action_title
from keyboards.reply.main_menu import generate_main_menu
from router import router
from constants import LastVisitedPlaces


@router.message(lambda message: message.text in ["👈 Orqaga", "👈 Назад", "👈 Back"])
async def back(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    last_visited_place = user.get("last_visited_place")

    await state.clear()

    if last_visited_place == LastVisitedPlaces.SETTINGS:
        await message.answer(text=f"{action_title.get(user.get("lang"))}", reply_markup=generate_main_menu(user.get("lang")))
