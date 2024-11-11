from aiogram import types, Router, F

from buttons.for_user import watch_movie_menu
from queries.for_account import AccountModel
from queries.for_like import LikeModel
from queries.for_movie import MovieModel
from queries.for_user import UserModel

movie_model = MovieModel()
user_model = UserModel()
account_model = AccountModel()
like_model = LikeModel()

router_for_like = Router()


@router_for_like.callback_query(F.data.startswith('like_'))
async def like_movie(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    try:
        user_id = call.data.split('_')[1].strip()
        movie_id = call.data.split('_')[2].strip()
        movie_data = movie_model.get_movie_by_id(movie_id)

        if user_id == 'None':
            await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                              show_alert=True)
            return

        if movie_data:
            if like_model.get_like_by_user_id_and_movie_id(user_id, movie_id):
                await call.answer(text=f"{movie_data['title']} - Siz Bu Videoga Allaqachon Like Bosgansiz✅")

            else:
                await call.answer(text=f"{movie_data['title']} - Like Bosildi✅")
                like_model.create_like(user_id, movie_id)

            new_markup = await watch_movie_menu(user_id, movie_id)
            await call.message.edit_reply_markup(reply_markup=new_markup)

        else:
            await call.answer("Bu film topilmadi ❌", show_alert=True)

    except Exception:
        await call.answer(f"Xatolik yuz berdi ❌", show_alert=True)


@router_for_like.callback_query(F.data.startswith('dislike_'))
async def dislike_movie(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    try:
        user_id, movie_id = map(int, call.data.split('_')[1:])
        movie_data = movie_model.get_movie_by_id(movie_id)

        if movie_data:
            if like_model.get_like_by_user_id_and_movie_id(user_id, movie_id):
                await call.answer(text=f"{movie_data['title']} - Like Olib Tashlandi✅")
                like_model.delete_like(user_id, movie_id)

                new_markup = await watch_movie_menu(user_id, movie_id)
                await call.message.edit_reply_markup(reply_markup=new_markup)

            else:
                await call.answer(text=f"{movie_data['title']} - Siz Bu Videoda Like Bosmagansiz ❌")

        else:
            await call.answer("Bu film topilmadi ❌", show_alert=True)

    except Exception:
        await call.answer(f"Xatolik yuz berdi ❌", show_alert=True)