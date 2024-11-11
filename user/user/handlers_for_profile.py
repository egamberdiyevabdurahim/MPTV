from aiogram import Router, F, types

from buttons.for_user import saveds_data_menu, \
    likes_data_menu, viewed_data_menu
from queries.for_account import AccountModel
from queries.for_like import LikeModel
from queries.for_movie import MovieModel
from queries.for_saved import SavedModel
from queries.for_user import UserModel
from queries.for_user_movie import UserMovieModel

router_for_profile = Router()

movie_model = MovieModel()
user_model = UserModel()
account_model = AccountModel()
saved_model = SavedModel()
like_model = LikeModel()
user_movie_model = UserMovieModel()


@router_for_profile.callback_query(F.data == "change_password")
async def change_password_callback(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    await call.answer(text="Bu Funksiya Tez Orada Ishga Tushadi🔥", show_alert=True)


@router_for_profile.callback_query(F.data == "logout")
async def logout_callback(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    account = account_model.get_account_by_telegram_id(call.from_user.id)
    if account:
        account_model.logout(call.from_user.id)
        await call.message.answer(text="Tizimdan Muvaffaqiyatli Chiqildi!")
        try:
            await call.message.delete()

        except Exception:
            pass


@router_for_profile.callback_query(F.data == "saveds")
async def saved_movies_callback(call: types.CallbackQuery,
                                page=1, page_size=10, user_id=None):
    if user_id is None:
        user_id = call.from_user.id
    if not account_model.is_account_registered(user_id):
        await call.answer(text="Bu Funksiyani Ishlatish Uchun Ro'yxatdan O'ting!", show_alert=True)
        return

    try:
        await call.answer()
        await call.message.delete()
    except Exception:
        pass

    account_data = account_model.get_account_by_telegram_id(user_id)
    user_id = user_model.get_user_by_id(account_data.get('user_id')).get("id")

    saved_datas = saved_model.get_saved_movies_by_user_id(user_id=user_id)
    total_saved_movies = len(saved_datas)
    page_size = int(page_size)
    total_pages = (total_saved_movies + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\nSaqlanglar:\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_saved_movies = saved_datas[start_index:end_index]

    counter = start_index
    for saved_data in current_saved_movies:
        counter += 1
        movie = movie_model.get_movie_by_id(saved_data["movie_id"])
        text_data += f"{counter}. {movie['title']}\n"

    await call.message.answer(text=text_data,
                              reply_markup=await saveds_data_menu(
                                  user_id=user_id,
                                  page=page,
                                  page_size=page_size
                              ))


@router_for_profile.callback_query(F.data == "likes")
async def likes_movies_callback(call: types.CallbackQuery,
                                page=1, page_size=10, user_id=None):
    if user_id is None:
        user_id = call.from_user.id
    if not account_model.is_account_registered(user_id):
        await call.answer(text="Bu Funksiyani Ishlatish Uchun Ro'yxatdan O'ting!", show_alert=True)
        return

    try:
        await call.answer()
        await call.message.delete()
    except Exception:
        pass

    account_data = account_model.get_account_by_telegram_id(user_id)
    user_id = user_model.get_user_by_id(account_data.get('user_id')).get("id")

    liked_datas = like_model.get_likes_by_user_id(user_id=user_id)
    total_saved_movies = len(liked_datas)
    page_size = int(page_size)
    total_pages = (total_saved_movies + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\nYoqtirilganlar:\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_saved_movies = liked_datas[start_index:end_index]

    counter = start_index
    for saved_data in current_saved_movies:
        counter += 1
        movie = movie_model.get_movie_by_id(saved_data["movie_id"])
        text_data += f"{counter}. {movie['title']}\n"

    await call.message.answer(text=text_data,
                              reply_markup=await likes_data_menu(
                                  user_id=user_id,
                                  page=page,
                                  page_size=page_size
                              ))


@router_for_profile.callback_query(F.data == "viewed")
async def viewed_movies_callback(call: types.CallbackQuery,
                                page=1, page_size=10, user_id=None):
    if user_id is None:
        user_id = call.from_user.id
    if not account_model.is_account_registered(user_id):
        await call.answer(text="Bu Funksiyani Ishlatish Uchun Ro'yxatdan O'ting!", show_alert=True)
        return

    try:
        await call.answer()
        await call.message.delete()
    except Exception:
        pass

    account_data = account_model.get_account_by_telegram_id(user_id)
    user_id = user_model.get_user_by_id(account_data.get('user_id')).get("id")

    viewed_datas = user_movie_model.get_watched_movies(user_id=user_id)
    total_saved_movies = len(viewed_datas)
    page_size = int(page_size)
    total_pages = (total_saved_movies + page_size - 1) // page_size
    page = int(page)
    text_data = f"-------------{page}/{total_pages}-------------\nKo'rilganlar:\n"

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_saved_movies = viewed_datas[start_index:end_index]

    counter = start_index
    for saved_data in current_saved_movies:
        counter += 1
        movie = movie_model.get_movie_by_id(saved_data["movie_id"])
        text_data += f"{counter}. {movie['title']}\n"

    await call.message.answer(text=text_data,
                              reply_markup=await viewed_data_menu(
                                  user_id=user_id,
                                  page=page,
                                  page_size=page_size
                              ))
