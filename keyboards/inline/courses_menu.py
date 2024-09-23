from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from loader import db


def generate_courses_categories_menu(lang: str) -> InlineKeyboardMarkup:
    """Generates and returns courses categories menu

    Args:
        lang (str): User's language

    Returns:
        ReplyKeyboardMarkup: courses categories menu
    """
    categories = db.get_categories()
    builder = InlineKeyboardBuilder()
    
    for category in categories:
        builder.button(text=f"{category.get(f'name_{lang}')}", callback_data=f"category_{category.get('id')}")

    builder.adjust(1)

    return builder.as_markup()
