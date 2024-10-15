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


@router.callback_query(lambda call: "send_homework" in call.data)
async def accept_homework(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_user_lang(call.from_user.id)
    user_id = int(call.data.split(":")[1])
    lesson_id = int(call.data.split(":")[2])

    await state.set_data({'lesson_id': lesson_id, 'user_id': user_id})
    await state.set_state(HomeworkForm.homework)
    await call.message.answer(text=f'{request_homework_text.get(lang)}', reply_markup=generate_back_menu(lang))


@router.message(HomeworkForm.homework)
async def send_homework_to_admins(message: types.Message, state: FSMContext):
    lang = db.get_user_lang(message.from_user.id)
    homework_state = await state.get_data()

    lesson_id = homework_state.get('lesson_id')
    user_id = homework_state.get('user_id')
    student = db.get_user(message.from_user.id)
    lesson = db.get_lesson(lesson_id)

    for tg_id in ADMINS:
        try:
            admin_lang = db.get_user(telegram_id=tg_id).get('lang')

            student_full_name = student.get('full_name')
            student_phone_number = student.get('phone_number')

            title = f"{homework_title.get(admin_lang)}\n\n{lesson_name.get(admin_lang)}: {lesson.get(f'title_{admin_lang}')} \n{FIO.get(admin_lang)}: {student_full_name}\n{phone_number.get(admin_lang)}: {student_phone_number}\n\n{homework_body.get(admin_lang)}: {message.text}"
            await bot.send_message(chat_id=tg_id, text=title, reply_markup=generate_accept_or_deny_homework_menu(admin_lang, user_id, lesson_id))
        except:
            pass
        
    await message.answer(text=f"{homework_send_to_admins.get(lang)}", reply_markup=generate_main_menu(lang, message.from_user.id))
