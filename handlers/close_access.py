import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from loader import db
from router import router
from localization.i18n import request_contact_number, invalid_phone_number_selected, successfully_done
from constants import ADMINS
from states.grant_or_close_access_forms import CloseAccessForm
from keyboards.reply.request_contact_menu import generate_request_contact_menu
from keyboards.reply.main_menu import generate_main_menu


@router.message(lambda message: message.text in ["❌ Ruxsatni yopish", "❌ Закрыть доступ", "❌ Close access"])
async def request_phone_number(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    lang = user.get('lang')

    if user.get('telegram_id') in ADMINS:
        await state.set_state(CloseAccessForm.phone_number)
        await message.answer(text=f"{request_contact_number.get(lang)}", reply_markup=generate_request_contact_menu(lang))


@router.message(CloseAccessForm.phone_number)
async def grant_access(message: types.Message, state: FSMContext):
    lang = db.get_user_lang(message.from_user.id)
    phone_number_pattern = r'^(\+?\d{1,4}[\s.-]?)?(\(?\d{1,4}\)?[\s.-]?)?[\d\s.-]{3,}$'
    phone_number = message.contact.phone_number if message.contact else message.text

    if not re.fullmatch(phone_number_pattern, phone_number) or (message.text and len(phone_number.strip()) < 13):
        await message.answer(text=f"{invalid_phone_number_selected.get(lang)}")
    else:
        phone_number = message.contact.phone_number if message.contact else message.text
        db.grant_or_close_access(phone_number.replace("+", "").replace(" ", "").strip(), 0)
        await state.clear()
        await message.answer(text=f"{successfully_done.get(lang)} ✅", reply_markup=generate_main_menu(lang, message.from_user.id))
