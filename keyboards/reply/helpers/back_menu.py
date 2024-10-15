from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from .back_button import generate_back_button


def generate_back_menu(lang: str) -> ReplyKeyboardMarkup:
    """Generates and returns a kyboard with only one back button

    Args:
        lang (str): user's language

    Returns:
        ReplyKeyboardMarkup: Kaeyboard with only one back button
    """
    builder = ReplyKeyboardBuilder()
    builder.add(
        generate_back_button(lang)
    )

    return builder.as_markup(resize_keyboard=True)
