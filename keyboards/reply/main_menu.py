from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from localization.i18n import main_menu_keyboard
from constants import ADMINS


def generate_main_menu(lang: str, telegram_id: int) -> ReplyKeyboardMarkup:
    """Generates and returns main menu
    
    Args:
        telegram_id (int): user's telegram id

    Returns:
        lang: User's selected language
        ReplyKeyboardMarkup: main menu keyboard
    """
    builder = ReplyKeyboardBuilder()

    for button_text in main_menu_keyboard.get(lang)[:-2]:
        builder.button(text=button_text)
    
    if telegram_id in ADMINS:
        builder.button(text=main_menu_keyboard.get(lang)[-2])
        builder.button(text=main_menu_keyboard.get(lang)[-1])

    builder.adjust(2)

    return builder.as_markup(resize_keyboard=True)
