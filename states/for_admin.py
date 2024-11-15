from aiogram.fsm.state import StatesGroup, State


# COMPANY
class AddCompany(StatesGroup):
    name = State()


class DeleteCompany(StatesGroup):
    name = State()


# COUNTRY
class AddCountry(StatesGroup):
    name = State()


class DeleteCountry(StatesGroup):
    name = State()


# GENRE
class AddGenre(StatesGroup):
    name = State()


class DeleteGenre(StatesGroup):
    name = State()


# LANGUAGE
class AddLanguage(StatesGroup):
    name = State()


class DeleteLanguage(StatesGroup):
    name = State()


# CATEGORY
class AddCategory(StatesGroup):
    name = State()


class DeleteCategory(StatesGroup):
    name = State()


# MOVIE
class AddMovie(StatesGroup):
    title = State()
    release_date = State()
    duration = State()
    code = State()
    category_id = State()
    company_ids = State()
    language_id = State()
    country_id = State()
    genre_ids = State()
    movie_id_360 = State()
    movie_id_480 = State()
    movie_id_720 = State()
    movie_id_1080 = State()


class DeleteMovie(StatesGroup):
    code = State()
    validate = State()


# SENDING MESSAGE
class SendingMessageAdmin(StatesGroup):
    message = State()
    photo = State()