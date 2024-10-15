from aiogram import types
from aiogram.fsm.context import FSMContext

from loader import db, bot
from router import router
from localization.i18n import request_homework_text, homework_send_to_admins, homework_title, phone_number, homework_body, FIO, lesson_name
from keyboards.reply.helpers.back_menu import generate_back_menu
from keyboards.reply.main_menu import generate_main_menu
from keyboards.inline.accept_or_deny_homework_menu import generate_accept_or_deny_homework_menu
from states.homework_form import HomeworkForm
from constants import ADMINS


@router.callback_query(lambda call: "accept_or_deny_homework" in call.data)
async def accept_homework(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_user_lang(call.from_user.id)
    action = call.data.split(":")[-3]
    user_id = int(call.data.split(":")[-2])
    lesson_id = int(call.data.split(":")[1])

    # db.grant_access_to_lesson(user_id, lesson_id)
    # GET lesson_id from lessons table and insert user_id to this row for this lesson to allow a user watch next lesson
    
