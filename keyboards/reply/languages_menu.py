from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def generate_languages_menu() -> ReplyKeyboardMarkup:
    """Generates and returns languages menu

    Returns:
        ReplyKeyboardMarkup: main menu keyboard
    """
    builder = ReplyKeyboardBuilder()
    builder.button(text="🇺🇿 O'zbek")
    builder.button(text="🇷🇺 Русский")
    builder.button(text="🇺🇸 English")

    return builder.as_markup(resize_keyboard=True)
