from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from localization.i18n import accept_or_deny_homework


def generate_accept_or_deny_homework_menu(lang: str) -> InlineKeyboardMarkup:
    """Generates and a keyboard with 2 buttons to accept or deny the homework

    Args:
        lang (str): user's language

    Returns:
        InlineKeyboardMarkup: Keyboard with 2 buttons to accept or deny the homework
    """
    builder = InlineKeyboardBuilder()
    
    for index, btn_text in enumerate(accept_or_deny_homework.get(lang), start=1):
        builder.button(text=btn_text, callback_data=f"accept_or_deny_homework:{'accept' if index == 1 else 'deny'}")
    
    builder.adjust(1)
    return builder.as_markup()