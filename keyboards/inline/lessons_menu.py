from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from loader import db
from localization.i18n import access_granted, access_denied, free_lesson


def generate_lessons_menu(lang: str, category_id: int, subscription_status: int) -> InlineKeyboardMarkup:
    """Generates and returns lessons keyboard

    Args:
        lang (str): user's language
        category_id (int): lessons' category
        subscription_status (int): user's subscription status

    Returns:
        InlineKeyboardMarkup: Lesson keyboard
    """
    builder = InlineKeyboardBuilder()
    lessons = db.get_lessons(category_id=category_id)

    for index, lesson in enumerate(lessons, start=1):
        # builder.button(text=f"{index}. {lesson.get(f'title_{lang}')}",
        #                callback_data=f"lesson_{lesson.get('id')}")
        if index == 1:
            builder.button(text=f"{lesson.get(f'title_{lang}')} ({free_lesson.get(lang)})",
                        callback_data=f"lesson_{lesson.get('id')}")
        else:
            if int(subscription_status) == 1:
                builder.button(text=f"{lesson.get(f'title_{lang}')} ({access_granted.get(lang)})",
                            callback_data=f"lesson_{lesson.get('id')}")
            else:
                builder.button(text=f"{lesson.get(f'title_{lang}')} ({access_denied.get(lang)})",
                            callback_data=f"lesson_{lesson.get('id')}")
                
    builder.adjust(1)
    return builder.as_markup()