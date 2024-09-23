from aiogram.fsm.state import StatesGroup, State


class PhoneNumberForm(StatesGroup):
    phone_number = State()
