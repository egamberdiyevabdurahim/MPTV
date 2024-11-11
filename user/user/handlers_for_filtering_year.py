from aiogram import Router, F, types

from buttons.for_user import year_filtering_data_menu, year_filtering_menu
from queries.for_account import AccountModel
from queries.for_movie import MovieModel

router_for_filtering_year = Router()

movie_model = MovieModel()
account_model = AccountModel()


@router_for_filtering_year.callback_query(F.data == "filter_by_release_year")
async def filter_by_year(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    await call.message.answer('Yil tanlang:', reply_markup=await year_filtering_menu())

@router_for_filtering_year.callback_query(F.data.startswith("year_"))
async def year_filter(call: types.CallbackQuery,
                         page=1, page_size=10, year=None):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    if year is None:
        year = call.data.split("_")[1].strip()
        try:
            await call.answer()
            await call.message.delete()
        except:
            pass
    movies = movie_model.get_movies_by_year(year)  # Assuming this is an async call
    total_movies = len(movies)
    page_size = int(page_size)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{year} - Filmlar:\n"

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
                              reply_markup=await year_filtering_data_menu(
                                  year=year,
                                  page=page,
                                  page_size=page_size
                              ))