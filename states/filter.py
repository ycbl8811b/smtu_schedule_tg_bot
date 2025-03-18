from aiogram.filters.state import State, StatesGroup

class Filter(StatesGroup):
    waiting = State()
    choosing_group = State()
    choosing_week = State()
    choosing_day = State()
    choosing_teacher = State()
    confirm_filter = State()