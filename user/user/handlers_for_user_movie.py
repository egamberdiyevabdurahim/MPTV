from aiogram import types, Router, F

from buttons.for_user import watch_movie_menu
from queries.for_account import AccountModel
from queries.for_movie import MovieModel
from queries.for_user import UserModel
from queries.for_user_movie import UserMovieModel

movie_model = MovieModel()
user_model = UserModel()
account_model = AccountModel()
user_movie_model = UserMovieModel()

router_for_user_movie = Router()


@router_for_user_movie.callback_query(F.data.startswith('mark_watched_movie_'))
async def mark_watched_movie(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    try:
        user_id = call.data.split('_')[3].strip()
        movie_id = call.data.split('_')[4].strip()
        movie_data = movie_model.get_movie_by_id(movie_id)

        if user_id == 'None':
            await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                              show_alert=True)
            return

        if movie_data:
            watch = user_movie_model.get_by_user_id_and_movie_id(user_id, movie_id)
            if watch:
                if watch.get("watched") is False:
                    await call.answer(text=f"{movie_data['title']} - Videoni Ko'rildi Deb Belgilandi✅")
                    user_movie_model.mark_as_watched(user_id, movie_id)

                else:
                    await call.answer(text=f"{movie_data['title']} - Siz Bu Videoni Allaqachon Ko'rildi Deb Belgilagansiz ❌")

            else:
                await call.answer(text=f"{movie_data['title']} - Videoni Ko'rildi Deb Belgilandi✅")
                user_movie_model.create_movie(user_id, movie_id)

            new_markup = await watch_movie_menu(user_id, movie_id)
            await call.message.edit_reply_markup(reply_markup=new_markup)

        else:
            await call.answer("Bu film topilmadi ❌", show_alert=True)

    except Exception:
        await call.answer(f"Xatolik yuz berdi ❌", show_alert=True)


@router_for_user_movie.callback_query(F.data.startswith('unmark_watched_movie_'))
async def unmark_watched_movie(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    try:
        user_id, movie_id = map(int, call.data.split('_')[3:])
        movie_data = movie_model.get_movie_by_id(movie_id)

        if movie_data:
            watch = user_movie_model.get_by_user_id_and_movie_id(user_id, movie_id)
            if watch:
                if watch.get("watched") is True:
                    await call.answer(text=f"{movie_data['title']} - Videoni Ko'rilmadi Deb Belgilandi✅")
                    user_movie_model.unmark_as_watched(user_id, movie_id)

                else:
                    await call.answer(text=f"{movie_data['title']} - Siz Bu Videoni Allaqachon Ko'rilmadi Deb Belgilagansiz ❌")

                new_markup = await watch_movie_menu(user_id, movie_id)
                await call.message.edit_reply_markup(reply_markup=new_markup)

        else:
            await call.answer("Bu film topilmadi ❌", show_alert=True)

    except Exception:
        await call.answer(f"Xatolik yuz berdi ❌", show_alert=True)
