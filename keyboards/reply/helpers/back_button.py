from aiogram.types import KeyboardButton

from localization.i18n import back_button


def generate_back_button(lang: str) -> KeyboardButton:
    """Generates and returns back button

    Args:
        lang (str): User's selected langugage

    Returns:
        KeyboardButton: back button object
    """
    button = KeyboardButton(text=f"{back_button.get(lang)}")
    return button
