from aiogram.dispatcher.filters.state import StatesGroup, State

class Questions(StatesGroup):
    yes_or_no = State()
    choice_area = State()
    input_phone_number = State()
    input_email = State()