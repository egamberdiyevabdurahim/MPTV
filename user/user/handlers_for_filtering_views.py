from aiogram import Router, F, types

from buttons.for_user import movie_views_data_menu
from queries.for_account import AccountModel
from queries.for_company import CompanyModel
from queries.for_movie import MovieModel

router_for_filtering_views = Router()

movie_model = MovieModel()
company_model = CompanyModel()
account_model = AccountModel()


@router_for_filtering_views.callback_query(F.data == "filter_by_views")
async def filter_by_views(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    movies = movie_model.get_most_viewed_movies(10)
    text_data = "Top 10 ta eng ko'p kor'ilganlar:\n\n"
    counter = 0
    for movie in movies:
        counter += 1
        text_data += f"{counter}. {movie['title']}\n"

    await call.message.answer(text=text_data,
                              reply_markup=await movie_views_data_menu(
                                  movies=movies
                              ))
