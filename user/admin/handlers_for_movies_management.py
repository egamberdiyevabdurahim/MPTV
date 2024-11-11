from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from buttons.for_admin import movie_management_menu, country_management_menu, company_management_menu, \
    genre_management_menu, language_management_menu, category_management_menu

from queries.for_account import AccountModel
from queries.for_user import UserModel
from utils.validator import my_validator

router_for_movies_management = Router()

user_model = UserModel()
account_model = AccountModel()


@router_for_movies_management.callback_query(F.data == 'movie_management')
async def movie_management(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    if state:
        await state.clear()

    await call.answer()
    await call.message.delete()
    await call.message.answer('Kino yoki Multfilm Boshqaruvi', reply_markup=movie_management_menu)


@router_for_movies_management.callback_query(F.data == 'company_management')
async def company_management(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Kompaniya Boshqaruvi', reply_markup=company_management_menu)


@router_for_movies_management.callback_query(F.data == 'country_management')
async def country_management(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Davlatlar Boshqaruvi', reply_markup=country_management_menu)


@router_for_movies_management.callback_query(F.data == 'genre_management')
async def genre_management(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Janr Boshqaruvi', reply_markup=genre_management_menu)


@router_for_movies_management.callback_query(F.data == 'language_management')
async def language_management(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Til Boshqaruvi', reply_markup=language_management_menu)


@router_for_movies_management.callback_query(F.data == 'category_management')
async def category_management(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Categoriya Boshqaruvi', reply_markup=category_management_menu)