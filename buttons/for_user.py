from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from queries.for_category import CategoryModel
from queries.for_company import CompanyModel
from queries.for_country import CountryModel
from queries.for_genre import GenreModel
from queries.for_language import LanguageModel
from queries.for_like import LikeModel
from queries.for_saved import SavedModel
from queries.for_user_movie import UserMovieModel
from user.admin.handlers_for_movie_management import movie_model

saved_model = SavedModel()
like_model = LikeModel()
user_movie_model = UserMovieModel()
company_model = CompanyModel()
category_model = CategoryModel()
genre_model = GenreModel()
language_model = LanguageModel()
country_model = CountryModel()


back_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_main")]
])


back_to_filtering_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_filtering")]
])


main_menu_un_auth = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Login", callback_data="login"), InlineKeyboardButton(text="Register", callback_data="register")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Kodi orqali topish", callback_data="movie_from_code")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Izlash", callback_data="movie_find")],
])


main_menu_auth = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Profil", callback_data="profile")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Kodi orqali topish", callback_data="movie_from_code")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Izlash", callback_data="movie_find")],
])


profile_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Parolni O'zgartirish", callback_data="change_password")],
    [InlineKeyboardButton(text="Tizimdan Chiqish", callback_data="logout")],
    [InlineKeyboardButton(text="Saqlanganlar🗂", callback_data="saveds")],
    [InlineKeyboardButton(text="Yoqtirilganlar❤️", callback_data="likes")],
    [InlineKeyboardButton(text="Ko'rilganlar👁", callback_data="viewed")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_main")],
])


async def quality_movie_menu(movie):
    markup = InlineKeyboardBuilder()

    if movie.get('movie_id_360'):
        markup.add(InlineKeyboardButton(text="360p", callback_data="360"))

    if movie.get('movie_id_480'):
        markup.add(InlineKeyboardButton(text="480p", callback_data="480"))

    if movie.get('movie_id_720'):
        markup.add(InlineKeyboardButton(text="720p", callback_data="720"))

    if movie.get('movie_id_1080'):
        markup.add(InlineKeyboardButton(text="1080p", callback_data="1080"))

    markup.adjust(2)
    return markup.as_markup()


async def watch_movie_menu(user_id, movie_id):
    markup = InlineKeyboardBuilder()
    if user_id is not None:
        # Fetch user-specific movie data
        user_movie = user_movie_model.get_by_user_id_and_movie_id(user_id, movie_id)
        saved = saved_model.get_saved_by_user_id_and_movie_id(user_id, movie_id)
        like = like_model.get_like_by_user_id_and_movie_id(user_id, movie_id)

    # Watched/Unwatched Button
        if user_movie is not None and user_movie['watched']:
            markup.row(
                InlineKeyboardButton(text="Ko'rilgan👁", callback_data=f"unmark_watched_movie_{user_id}_{movie_id}")
            )
        else:
            markup.row(
                InlineKeyboardButton(text="Ko'rilmagan🔴", callback_data=f"mark_watched_movie_{user_id}_{movie_id}")
            )

        # Saved/Unsaved Button
        if saved is not None:
            markup.row(
                InlineKeyboardButton(text="Saqlangan🗂", callback_data=f"un_save_movie_{user_id}_{movie_id}")
            )
        else:
            markup.row(
                InlineKeyboardButton(text="Saqlash📂", callback_data=f"save_movie_{user_id}_{movie_id}")
            )

        # Like/Dislike Button
        if like is not None:
            markup.row(
                InlineKeyboardButton(text="❤️", callback_data=f"dislike_{user_id}_{movie_id}")
            )
        else:
            markup.row(
                InlineKeyboardButton(text="🖤", callback_data=f"like_{user_id}_{movie_id}")
            )

    else:
        markup.row(
            InlineKeyboardButton(text="Ko'rilmagan🔴", callback_data=f"mark_watched_movie_{user_id}_{movie_id}")
        )
        markup.row(
            InlineKeyboardButton(text="Saqlash📂", callback_data=f"save_movie_{user_id}_{movie_id}")
        )
        markup.row(
            InlineKeyboardButton(text="🖤", callback_data=f"like_{user_id}_{movie_id}")
        )

    # Return the InlineKeyboardMarkup
    return markup.as_markup()


before_filtering_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Kino yoki Multfilm Nomi orqali izlash", callback_data="movie_from_title")],
    [InlineKeyboardButton(text="Studiya bo'yicha filterlash", callback_data="filter_by_company")],
    [InlineKeyboardButton(text="Til bo'yicha filterlash", callback_data="filter_by_language")],
    [InlineKeyboardButton(text="Davlat bo'yicha filterlash", callback_data="filter_by_country")],
    [InlineKeyboardButton(text="Janr bo'yicha filterlash", callback_data="filter_by_genre")],
    [InlineKeyboardButton(text="Yili bo'yicha filterlash", callback_data="filter_by_release_year")],
    [InlineKeyboardButton(text="Kategoriya bo'yicha filterlash", callback_data="filter_by_category")],
    [InlineKeyboardButton(text="Eng ko'p yoqtirilganlar❤️", callback_data="filter_by_likes")],
    [InlineKeyboardButton(text="Eng ko'p ko'rilganlar👁‍", callback_data="filter_by_views")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_main")]
])


async def company_filtering_menu():
    markup = InlineKeyboardBuilder()
    companies = company_model.get_all_companies()
    for company in companies:
        markup.add(InlineKeyboardButton(text=company['name'],
                                        callback_data=f"company_{company['id']}"))

    markup.adjust(3)
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))
    return markup.as_markup()


async def language_filtering_menu():
    markup = InlineKeyboardBuilder()
    languages = language_model.get_all_languages()
    for language in languages:
        markup.add(InlineKeyboardButton(text=language['name'],
                                        callback_data=f"language_{language['id']}"))

    markup.adjust(2)
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))
    return markup.as_markup()


async def country_filtering_menu():
    markup = InlineKeyboardBuilder()
    countries = country_model.get_all_countries()
    for country in countries:
        markup.add(InlineKeyboardButton(text=country['name'], callback_data=f"country_{country['id']}"))

    markup.adjust(2)
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))
    return markup.as_markup()


async def genre_filtering_menu():
    markup = InlineKeyboardBuilder()
    genres = genre_model.get_all_genres()
    for genre in genres:
        markup.add(InlineKeyboardButton(text=genre['name'], callback_data=f"genre_{genre['id']}"))

    markup.adjust(3)
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))
    return markup.as_markup()


async def category_filtering_menu():
    markup = InlineKeyboardBuilder()
    categories = category_model.get_all_categories()
    for category in categories:
        markup.add(InlineKeyboardButton(text=category['name'], callback_data=f"category_{category['id']}"))

    markup.adjust(1)
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))
    return markup.as_markup()


async def year_filtering_menu():
    markup = InlineKeyboardBuilder()
    years = movie_model.get_movies_year()
    for year in years:
        markup.add(InlineKeyboardButton(text=f"{year['release_date']} ({year['counter']})",
                                        callback_data=f"year_{year['release_date']}"))

    markup.adjust(3)
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))
    return markup.as_markup()


async def company_filtering_data_menu(company_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_company_id(company_id)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)

    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_company_{company_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_company_{company_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def language_filtering_data_menu(language_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_language_id(language_id)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_language_{language_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_language_{language_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def category_filtering_data_menu(category_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_category_id(category_id)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_category_{category_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_category_{category_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def genre_filtering_data_menu(genre_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_genre_id(genre_id)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_genre_{genre_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_genre_{genre_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def country_filtering_data_menu(country_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_country_id(country_id)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_country_{country_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_country_{country_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def year_filtering_data_menu(year, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_year(year)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_year_{year}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_year_{year}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def movie_search_data_menu(text, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = movie_model.get_movies_by_search(text)  # Assuming this is an async call
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)

    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)

    # Add navigation buttons if there are multiple pages
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_search_{text}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_search_{text}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def movie_likes_data_menu(movies):
    markup = InlineKeyboardBuilder()

    # Add movie buttons
    counter = 0
    for movie in movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def movie_views_data_menu(movies):
    markup = InlineKeyboardBuilder()

    # Add movie buttons
    counter = 0
    for movie in movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['id']}"))

    markup.adjust(5)
    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_filtering'))

    return markup.as_markup()


async def saveds_data_menu(user_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = saved_model.get_saved_movies_by_user_id(user_id=user_id)
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size
    page = int(page)

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['movie_id']}"))

    markup.adjust(5)

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_saveds_{user_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_saveds_{user_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_profile'))

    return markup.as_markup()


async def likes_data_menu(user_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = like_model.get_likes_by_user_id(user_id=user_id)
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size
    page = int(page)

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['movie_id']}"))

    markup.adjust(5)

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_likes_{user_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_likes_{user_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_profile'))

    return markup.as_markup()


async def viewed_data_menu(user_id, page=1, page_size=10):
    markup = InlineKeyboardBuilder()
    movies = user_movie_model.get_watched_movies(user_id=user_id)
    total_movies = len(movies)
    total_pages = (total_movies + page_size - 1) // page_size
    page = int(page)

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    counter = start_index
    for movie in current_movies:
        counter += 1
        markup.add(InlineKeyboardButton(text=f"{counter}",
                                        callback_data=f"movie_filtering_{movie['movie_id']}"))

    markup.adjust(5)

    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text="⬅️",
                                                       callback_data=f"page_{page - 1}_viewed_{user_id}"))
    # navigation_buttons.append(InlineKeyboardButton(text=f"{page}/{total_pages}"))
    if page < total_pages:
        navigation_buttons.append(InlineKeyboardButton(text="➡️",
                                                       callback_data=f"page_{page + 1}_viewed_{user_id}"))

    # Add navigation buttons in a row
    markup.row(*navigation_buttons)

    # Add the back button
    markup.row(InlineKeyboardButton(text='Ortga', callback_data='back_to_profile'))

    return markup.as_markup()
