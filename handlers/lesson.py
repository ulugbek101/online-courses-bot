from aiogram import types
from aiogram.enums import ChatAction

from loader import db, bot
from router import router
from localization.i18n import payment_required, complete_homework_warning
from keyboards.inline.send_homework_menu import generate_send_homework_menu


@router.callback_query(lambda call: "lesson" in call.data)
async def handler(call: types.CallbackQuery):
    lesson_id = int(call.data.split("_")[-1])

    user = db.get_user(call.from_user.id)
    lang = user.get('lang')
    lesson = db.get_lesson(lesson_id)
    chat_action = ChatAction.UPLOAD_VIDEO

    if lesson.get('payment_required') == 1 and user.get('is_subscribed') == 0:
        await call.answer(text=payment_required.get(lang), show_alert=True)
    else:
        homeworks_list = db.get_users_done_homeworks(user.get('id')) or ""
        homeworks_list = homeworks_list.split(",")

        # TODO: Change the second part of if statement to be equal to 1 or to other id in case if the first lesson's if of advances lessons will be another id
        if str(lesson.get('id')) == homeworks_list[-1] or lesson.get('id') == 1:
            await bot.send_chat_action(chat_id=call.from_user.id, action=chat_action)
            await call.message.answer_video(video=lesson.get('file_id'), caption=f"{lesson.get(f'title_{lang}')}", reply_markup=generate_send_homework_menu(lang=lang, user_id=user.get('id'), lesson_id=lesson.get('id')))
        else:
            await call.answer(text=f"{complete_homework_warning.get(lang)}", show_alert=True)
