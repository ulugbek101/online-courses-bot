from aiogram import types

from loader import db
from router import router
from localization.i18n import action_title
from keyboards.inline.lessons_menu import generate_lessons_menu


@router.callback_query(lambda call: "category" in call.data)
async def show_categories(call: types.CallbackQuery):
    user = db.get_user(call.from_user.id)
    lang = user.get('lang')
    category_id = int(call.data.split("_")[-1])

    await call.message.answer(text=f"{action_title.get(lang)}", reply_markup=generate_lessons_menu(lang, category_id, user.get('is_subscribed')))
