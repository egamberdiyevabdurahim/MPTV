from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from buttons.for_admin import admin_panel_menu, movies_management_menu, user_management_menu
from queries.for_account import AccountModel
from queries.for_user import UserModel
from utils.validator import my_validator

router_for_admin = Router()

account_model = AccountModel()
user_model = UserModel()


@router_for_admin.callback_query(F.data == "back_to_admin")
async def back_to_admin(call: types.CallbackQuery):
    await admin_panel(call)


@router_for_admin.callback_query(F.data == 'back_to_movies')
async def back_to_movies(call: types.CallbackQuery):
    await movies_management(call)


@router_for_admin.callback_query(F.data == 'admin')
async def admin_panel(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Admin panel', reply_markup=admin_panel_menu)


@router_for_admin.callback_query(F.data == 'user_management')
async def user_management(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer('Userlar Boshqaruvi', reply_markup=user_management_menu)


@router_for_admin.callback_query(F.data == 'movies_management')
async def movies_management(call: types.CallbackQuery=None, message: types.Message=None, state: FSMContext=None,
                            delete=True):
    await my_validator(message=call.message, user=call.from_user)
    if state:
        await state.clear()

    if call:
        await call.answer()
        if delete:
            await call.message.delete()
        await call.message.answer("Kino yoki Multfilm Boshqaruvi(Asosiy)", reply_markup=movies_management_menu)

    elif message:
        if delete:
            await message.delete()
        await message.answer("Kino yoki Multfilm Boshqaruvi(Asosiy)", reply_markup=movies_management_menu)