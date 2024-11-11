from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    username = State()
    password = State()
    back = State()


class LoginState(StatesGroup):
    username = State()
    password = State()
    back = State()
