from aiogram import types

from loader import db, bot
from router import router
from localization.i18n import homework_accepted, successfully_done, lesson_name


@router.callback_query(lambda call: "accept_or_deny_homework" in call.data)
async def accept_homework(call: types.CallbackQuery):
    lang = db.get_user_lang(call.from_user.id)
    action = call.data.split(":")[1]
    user_id = int(call.data.split(":")[2])
    lesson_id = int(call.data.split(":")[3])

    # Get user from users table
    user = db.get_user_by_id(user_id)
    lesson = db.get_lesson(lesson_id)
    user_lang = user.get('lang')

    if action == "accept":
        # Insert lesson id to the homeworks_done column of a user
        db.update_user_homework(user_id, lesson_id)
        # Send a message to a user
        text = ""
        text += f"{homework_accepted.get(user_lang)}\n"
        text += f"{lesson_name.get(user_lang)}: {lesson.get(f'title_{user_lang}')}"

        await bot.send_message(chat_id=user.get('telegram_id'), text=text)
        await call.message.answer(text=f"{successfully_done.get(lang)}")
        await call.message.delete()
    # db.grant_access_to_lesson(user_id, lesson_id)
    # GET lesson_id from lessons table and insert user_id to this row for this lesson to allow a user watch next lesson
    
