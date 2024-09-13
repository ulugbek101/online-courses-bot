from aiogram import types
from aiogram.fsm.context import FSMContext

from loader import db
from localization.i18n import action_title, invalid_language_selected, successfully_done
from keyboards.reply.languages_menu import generate_languages_menu
from keyboards.reply.settings_menu import generate_settings_menu
from states.languages_form import UpdateLanguageForm
from router import router


@router.message(lambda message: message.text in ["🇺🇿 Tilni o'zgartirish", "🇷🇺 Изменить язык", "🇺🇸 Change language"])
async def change_language(message: types.Message, state: FSMContext):
    lang = db.get_user_lang(message.from_user.id)

    await state.set_state(UpdateLanguageForm.lang)
    await message.answer(text=f"{action_title.get(lang)}", reply_markup=generate_languages_menu())


@router.message(UpdateLanguageForm.lang)
async def update_language(message: types.Message, state: FSMContext):
    lang = db.get_user_lang(message.from_user.id)

    if message.text not in ["🇺🇿 O'zbek", "🇷🇺 Русский", "🇺🇸 English"]:
        await message.answer(text=f"{invalid_language_selected.get(lang)}")
    else:
        languages_set = {
            "🇺🇿 O'zbek": "uz",
            "🇷🇺 Русский": "ru",
            "🇺🇸 English": "en"
        }
        selected_lang = languages_set.get(message.text)
        db.update_language(selected_lang, message.from_user.id)
        await state.clear()
        await message.answer(text=f"{successfully_done.get(selected_lang)} ✅", reply_markup=generate_settings_menu(selected_lang))
