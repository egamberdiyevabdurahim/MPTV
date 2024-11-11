from aiogram import types, Router, F

from buttons.for_user import watch_movie_menu
from queries.for_account import AccountModel
from queries.for_movie import MovieModel
from queries.for_saved import SavedModel
from queries.for_user import UserModel

movie_model = MovieModel()
user_model = UserModel()
account_model = AccountModel()
saved_model = SavedModel()

router_for_saved = Router()


@router_for_saved.callback_query(F.data.startswith('save_movie_'))
async def save_movie(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    try:
        user_id = call.data.split('_')[2].strip()
        movie_id = call.data.split('_')[3].strip()
        movie_data = movie_model.get_movie_by_id(movie_id)

        if user_id == 'None':
            await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                              show_alert=True)
            return

        if movie_data:
            if saved_model.get_saved_by_user_id_and_movie_id(user_id, movie_id):
                await call.answer(text=f"{movie_data['title']} - Siz Bu Videoni Allaqachon Saqlagansiz")

            else:
                await call.answer(text=f"{movie_data['title']} - Saqlandi✅")
                saved_model.create_saved(user_id=user_id, movie_id=movie_id)

            new_markup = await watch_movie_menu(user_id, movie_id)
            await call.message.edit_reply_markup(reply_markup=new_markup)
        else:
            await call.answer("Bu film topilmadi ❌", show_alert=True)

    except Exception:
        await call.answer("Xatolik yuz berdi ❌", show_alert=True)


@router_for_saved.callback_query(F.data.startswith('un_save_movie_'))
async def un_save_movie(call: types.CallbackQuery):
    account = account_model.is_account_registered(call.from_user.id)
    if not account:
        await call.answer(text=f"Bu Funksiyani Ishlatish Uchun Avval Ro'yxatdan O'ting!",
                          show_alert=True)
        return
    try:
        user_id, movie_id = map(int, call.data.split('_')[3:])
        movie_data = movie_model.get_movie_by_id(movie_id)

        if movie_data:
            await call.answer(f"{movie_data.get('title')} - Saqlanganlardan O'chirildi✅")
            saved_model.delete_saved(user_id=user_id, movie_id=movie_id)

            new_markup = await watch_movie_menu(user_id, movie_id)
            await call.message.edit_reply_markup(reply_markup=new_markup)
        else:
            await call.answer("Bu film topilmadi ❌", show_alert=True)

    except Exception:
        await call.answer("Xatolik yuz berdi ❌", show_alert=True)
