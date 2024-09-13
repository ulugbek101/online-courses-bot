from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from localization.i18n import settings_menu_keyboard
from .helpers.back_button import generate_back_button


def generate_settings_menu(lang: str) -> ReplyKeyboardMarkup:
    """Generates and returns settings menu

    Args:
        lang (str): User's selected language

    Returns:
        ReplyKeyboardMarkup: settings menu
    """
    builder = ReplyKeyboardBuilder()

    for button_text in settings_menu_keyboard.get(lang):
        builder.button(text=button_text)
    builder.adjust(2)

    back_button = generate_back_button(lang)
    builder.row(back_button)

    return builder.as_markup(resize_keyboard=True)
