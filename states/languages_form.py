from aiogram.fsm.state import StatesGroup, State


class LanguagesForm(StatesGroup):
    lang = State()
