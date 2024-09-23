from aiogram import types

from loader import db
from router import router
from localization.i18n import select_course_category
from keyboards.inline.courses_menu import generate_courses_categories_menu


@router.message(lambda message: message.text in ["📋 Kurslar", "📋 Курсы", "📋 Courses"])
async def courses(message: types.Message):
    lang = db.get_user_lang(message.from_user.id)
    photo = types.FSInputFile("media/about_me.jpg")
    
    await message.answer_photo(
        photo=photo,
        caption=f"{select_course_category.get(lang)}",
        reply_markup=generate_courses_categories_menu(lang)
    )
