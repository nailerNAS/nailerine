from aiogram.dispatcher.filters.state import State, StatesGroup


class Login(StatesGroup):
    session = State()
    api_id = State()
    api_hash = State()
    number = State()
    code = State()
    password = State()
