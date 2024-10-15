from aiogram.fsm.state import StatesGroup, State


class HomeworkForm(StatesGroup):
    homework = State()
    user_id = State()
    lesson_id = State()
