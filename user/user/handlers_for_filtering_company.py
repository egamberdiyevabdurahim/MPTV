from aiogram import Router, F, types

from buttons.for_user import company_filtering_data_menu, company_filtering_menu
from queries.for_account import AccountModel
from queries.for_company import CompanyModel
from queries.for_movie import MovieModel

router_for_filtering_company = Router()

movie_model = MovieModel()
company_model = CompanyModel()
account_model = AccountModel()


@router_for_filtering_company.callback_query(F.data == "filter_by_company")
async def filter_by_company(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    await call.answer()
    await call.message.delete()
    await call.message.answer('Studiyani tanlang:', reply_markup=await company_filtering_menu())

@router_for_filtering_company.callback_query(F.data.startswith("company_"))
async def company_filter(call: types.CallbackQuery,
                         page=1, page_size=10, company_id=None):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    if company_id is None:
        company_id = call.data.split("_")[1].strip()
        await call.answer()
        await call.message.delete()
    company_data = company_model.get_company_by_id(company_id)
    movies = movie_model.get_movies_by_company_id(company_id)  # Assuming this is an async call
    total_movies = len(movies)
    page_size = int(page_size)
    total_pages = (total_movies + page_size - 1) // page_size  # Calculate total pages
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\n{company_data['name']} - Filmlar:\n"

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
                              reply_markup=await company_filtering_data_menu(
                                  company_id=company_id,
                                  page=page,
                                  page_size=page_size
                              ))