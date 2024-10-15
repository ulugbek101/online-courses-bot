from aiogram.fsm.state import StatesGroup, State


class GratAccessForm(StatesGroup):
    phone_number = State()


class CloseAccessForm(StatesGroup):
    phone_number = State()
