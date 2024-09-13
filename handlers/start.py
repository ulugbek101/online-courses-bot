from aiogram import types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from router import router
from localozation.i18n import greeting, select_language, invalid_language_selected, successfull_registration
from states.languages_form import LanguagesForm
from loader import db
from keyboards.reply.languages_menu import generate_languages_menu
from keyboards.reply.main_menu import generate_main_menu


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
    await state.set_state(LanguagesForm.lang)
    await message.answer(text=f"{greeting.get(lang)} {select_language.get(lang)}".format(message.from_user.full_name), reply_markup=generate_languages_menu())


@router.message(LanguagesForm.lang)
async def completeregistration(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code

    if message.text not in ["🇺🇿 O'zbek", "🇷🇺 Русский", "🇺🇸 English"]:
        await message.answer(text=f"{invalid_language_selected.get(lang)}")
    else:
        languages_set = {
            "🇺🇿 O'zbek": "uz",
            "🇷🇺 Русский": "ru",
            "🇺🇸 English": "en"
        }
        selected_lang = languages_set.get(message.text)
        db.register_user(telegram_id=message.from_user.id,
                         full_name=message.from_user.full_name,
                         username=message.from_user.username,
                         lang=selected_lang)
        await message.answer(text=f"{successfull_registration.get(lang)} ✅", reply_markup=generate_main_menu(lang=selected_lang))
