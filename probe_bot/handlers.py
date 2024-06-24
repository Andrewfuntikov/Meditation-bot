from aiogram.fsm.state import StatesGroup, State


class StepsForm(StatesGroup):
    FILE_NAME = State()
    COUNT_FILE = State()