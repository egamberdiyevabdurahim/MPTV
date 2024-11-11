from aiogram import Router, F, types

from buttons.for_user import genre_filtering_data_menu, genre_filtering_menu
from queries.for_account import AccountModel
from queries.for_genre import GenreModel
from queries.for_movie import MovieModel

router_for_filtering_genre = Router()

movie_model = MovieModel()
genre_model = GenreModel()
account_model = AccountModel()


@router_for_filtering_genre.callback_query(F.data == "filter_by_genre")
async def filter_by_genre(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    await call.message.answer('Janr tanlang:', reply_markup=await genre_filtering_menu())

@router_for_filtering_genre.callback_query(F.data.startswith("genre_"))
async def genre_filter(call: types.CallbackQuery,
                         page=1, page_size=10, genre_id=None):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    if genre_id is None:
        genre_id = call.data.split("_")[1].strip()
        try:
            await call.answer()
            await call.message.delete()
        except:
            pass
    genre_data = genre_model.get_genre_by_id(genre_id)
    movies = movie_model.get_movies_by_genre_id(genre_id)  # Assuming this is an async call
    total_movies = len(movies)
    page_size = int(page_size)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{genre_data['name']} - Filmlar:\n"

    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        text_data += f"{counter}. {movie['title']}\n"

    await call.message.answer(text=text_data,
                              reply_markup=await genre_filtering_data_menu(
                                  genre_id=genre_id,
                                  page=page,
                                  page_size=page_size
                              ))