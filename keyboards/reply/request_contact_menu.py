from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from localization.i18n import request_contact_number_button
from .helpers.back_button import generate_back_button


def generate_request_contact_menu(lang: str) -> ReplyKeyboardMarkup:
    """Generates and returns a menu to request user's contact number

    Args:
        lang (str): User's language

    Returns:
        ReplyKeyboardMarkup: Request contact number menu
    """
    builder = ReplyKeyboardBuilder()
    builder.button(text=f"{request_contact_number_button.get(lang)}",
                   request_contact=True)
    back_button = generate_back_button(lang)
    builder.row(back_button)

    return builder.as_markup(resize_keyboard=True)
