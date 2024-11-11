from aiogram.fsm.state import StatesGroup, State


class MovieFromCodeState(StatesGroup):
    code = State()
    quality = State()


class FindMovieByTitleState(StatesGroup):
    title = State()