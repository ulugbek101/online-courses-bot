from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from localozation.i18n import main_menu_keyboard


def generate_main_menu(lang: str) -> ReplyKeyboardMarkup:
    """Generates and returns main menu

    Returns:
        lang: User's selected language
        ReplyKeyboardMarkup: main menu keyboard
    """
    builder = ReplyKeyboardBuilder()

    for button_text in main_menu_keyboard.get(lang):
        builder.button(text=button_text)
    builder.adjust(2)

    return builder.as_markup(resize_keyobard=True)
