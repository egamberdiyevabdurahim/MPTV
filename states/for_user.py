from aiogram.fsm.state import StatesGroup, State


class MovieFromCodeState(StatesGroup):
    code = State()
    quality = State()
    end = State()


class FindMovieByTitleState(StatesGroup):
    title = State()