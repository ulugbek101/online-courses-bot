from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from localization.i18n import send_homework


def generate_send_homework_menu(lang: str, user_id: int, lesson_id: int) -> InlineKeyboardMarkup:
    """Generates and returns a keyboard with only one button in it to send homework for a lesson to admins

    Args:
        lang (str): user's language
        user_id (int): user's id
        lesson_id (int): lesson's id

    Returns:
        InlineKeyboardMarkup: Send homework keyboard
    """
    builder = InlineKeyboardBuilder()

    builder.button(
        text=f"{send_homework.get(lang)}",
        callback_data=f"send_homework:{user_id}:{lesson_id}",
    )

    return builder.as_markup()