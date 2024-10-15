import re

from aiogram import types
from aiogram.fsm.context import FSMContext

from loader import db
from localization.i18n import request_contact_number, invalid_phone_number_selected, successfully_done
from keyboards.reply.request_contact_menu import generate_request_contact_menu
from keyboards.reply.settings_menu import generate_settings_menu
from states.phone_number_form import PhoneNumberForm
from router import router
from constants import LastVisitedPlaces


@router.message(lambda message: message.text in ["📞 Raqam kiritish/yangilash", "📞 Добавить/изменить номер", "📞 Add/change number"])
async def change_phone_number(message: types.Message, state: FSMContext):
    lang = db.get_user_lang(message.from_user.id)

    db.update_last_visited_place(LastVisitedPlaces.CHANGE_LANGUAGE,
                                 message.from_user.id)
    await state.set_state(PhoneNumberForm.phone_number)
    await message.answer(text=f"{request_contact_number.get(lang)}", reply_markup=generate_request_contact_menu(lang))


@router.message(PhoneNumberForm.phone_number)
async def update_language(message: types.Message, state: FSMContext):
    lang = db.get_user_lang(message.from_user.id)
    phone_number_pattern = r'^(\+?\d{1,4}[\s.-]?)?(\(?\d{1,4}\)?[\s.-]?)?[\d\s.-]{3,}$'
    phone_number = message.contact.phone_number if message.contact else message.text

    if not re.fullmatch(phone_number_pattern, phone_number):
        await message.answer(text=f"{invalid_phone_number_selected.get(lang)}")
    else:
        phone_number = message.contact.phone_number if message.contact else message.text
        db.update_phone_number(phone_number.replace("+", "").replace(" ", "").strip(), message.from_user.id)
        await state.clear()
        await message.answer(text=f"{successfully_done.get(lang)} ✅", reply_markup=generate_settings_menu(lang))
