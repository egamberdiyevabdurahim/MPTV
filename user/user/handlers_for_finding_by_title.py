from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from buttons.for_user import movie_search_data_menu, back_to_filtering_button
from queries.for_account import AccountModel
from queries.for_movie import MovieModel
from states.for_user import FindMovieByTitleState

router_for_finding_by_title = Router()

movie_model = MovieModel()
account_model = AccountModel()


@router_for_finding_by_title.callback_query(F.data == "movie_from_title")
async def find_movie_by_title(call: types.CallbackQuery, state: FSMContext):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    await call.message.answer("Filming nomini kiriting:", reply_markup=back_to_filtering_button)
    await state.set_state(FindMovieByTitleState.title)


@router_for_finding_by_title.message(FindMovieByTitleState.title)
async def find_movie_by_title_title(message: types.Message,
                                     page=1, page_size=10, text=None):
    account = account_model.is_account_registered(message.from_user.id)
    if not account:
        await message.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!")
        return
    if text is None:
        text = message.text

    movies = movie_model.get_movies_by_search(message.text)

    total_movies = len(movies)
    page_size = int(page_size)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{message.text} - Filmlar:\n"

    # Get the movies for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_movies = movies[start_index:end_index]

    # Add movie buttons
    counter = start_index
    for movie in current_movies:
        counter += 1
        text_data += f"{counter}. {movie['title']}\n"

    await message.answer(text=text_data,
                         reply_markup=await movie_search_data_menu(
                             text=text,
                             page=page,
                             page_size=page_size
                         ))