from aiogram.fsm.state import StatesGroup, State


class LanguagesForm(StatesGroup):
    lang = State()


class UpdateLanguageForm(StatesGroup):
    lang = State()
