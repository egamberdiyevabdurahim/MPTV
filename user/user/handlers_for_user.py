from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from buttons.for_user import before_filtering_menu, profile_menu
from queries.for_account import AccountModel
from user.user.handlers_for_filtering_category import category_filter
from user.user.handlers_for_filtering_company import company_filter
from user.user.handlers_for_filtering_country import country_filter
from user.user.handlers_for_filtering_genre import genre_filter
from user.user.handlers_for_filtering_language import language_filter
from user.user.handlers_for_filtering_year import year_filter
from user.user.handlers_for_finding_by_title import find_movie_by_title_title
from user.user.handlers_for_profile import saved_movies_callback, likes_movies_callback, viewed_movies_callback

router_for_user = Router()

account_model = AccountModel()


@router_for_user.callback_query(F.data == "movie_find")
async def movie_find(call: types.CallbackQuery, state: FSMContext, delete=True):
    if state:
        await state.clear()

    await call.answer()
    if delete:
        await call.message.delete()
    await call.message.answer('Kino yoki Multfilm izlash:', reply_markup=before_filtering_menu)


@router_for_user.callback_query(F.data == "profile")
async def profile_callback(call: types.CallbackQuery, state: FSMContext, delete=True):
    if state:
        await state.clear()

    if not account_model.is_account_registered(call.from_user.id):
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return

    await call.answer()
    try:
        if delete:
            await call.message.delete()

    except Exception:
        pass

    await call.message.answer(text=f"{call.from_user.first_name}ning Profili:",
                              reply_markup=profile_menu)


@router_for_user.callback_query(F.data == "back_to_filtering")
async def back_to_filtering(call: types.CallbackQuery, state: FSMContext, delete=True):
    await movie_find(call, state, delete)


@router_for_user.callback_query(F.data == "back_to_profile")
async def back_to_profile(call: types.CallbackQuery, state: FSMContext, delete=True):
    await profile_callback(call, state, delete)


@router_for_user.callback_query(F.data.startswith("page_"))
async def page_callback(call: types.CallbackQuery, state: FSMContext, delete=True):
    await call.answer()
    if delete:
        await call.message.delete()

    page = call.data.split("_")[1]
    type_data = call.data.split("_")[2]
    type_id = call.data.split("_")[-1]

    if type_data == "company":
        await company_filter(call=call, page=page, company_id=type_id)

    elif type_data == "category":
        await category_filter(call=call, page=page, category_id=type_id)

    elif type_data == "genre":
        await genre_filter(call=call, page=page, genre_id=type_id)

    elif type_data == "language":
        await language_filter(call=call, page=page, language_id=type_id)

    elif type_data == "country":
        await country_filter(call=call, page=page, country_id=type_id)

    elif type_data == "year":
        await year_filter(call=call, page=page, year_id=type_id)

    elif type_data == "search":
        await find_movie_by_title_title(message=call.message, state=state,
                                        page=page, text=type_id)

    # PROFILE
    elif type_data == "saveds":
        await saved_movies_callback(call=call,
                                    page=page, user_id=type_id)

    elif type_data == "likes":
        await likes_movies_callback(call=call,
                                    page=page, user_id=type_id)

    elif type_data == "viewed":
        await viewed_movies_callback(call=call,
                                     page=page, user_id=type_id)