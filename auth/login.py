from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from main import start_command
from buttons.for_user import back_button

from queries.for_account import AccountModel
from queries.for_user import UserModel

from states.for_auth import LoginState
from utils.validator import my_validator

account_model = AccountModel()
user_model = UserModel()

login_router = Router()


@login_router.callback_query(LoginState.back)
async def back_to_menu(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.clear()
    await start_command(call.message, user=call.from_user)


@login_router.callback_query(F.data == "login")
async def login1(call: types.CallbackQuery, state: FSMContext):
    account = account_model.is_account_registered(call.from_user.id)
    if account:
        await call.answer(text=f"Siz ALlaqachon Ro'yxatdan O'tgansiz!",
                          show_alert=True)
        return
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer(text="Username kiriting:", reply_markup=back_button)
    await state.set_state(LoginState.username)


@login_router.message(LoginState.username)
async def login2(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer(text="Username bo'sh bo'lishi mumkin emas!")
        await start_command(message, state=state)
        return

    await state.update_data(username=message.text.lower().strip())
    await message.answer(text="Parol Kiriting:", reply_markup=back_button)
    await state.set_state(LoginState.password)


@login_router.message(LoginState.password)
async def login3(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer(text="Parol bo'sh bo'lishi mumkin emas!")
        await start_command(message, state=state)
        return

    await state.update_data(password=message.text.strip())
    state_data = await state.get_data()
    user = user_model.get_user_by_username_and_password(username=state_data['username'],
                                                        password=state_data['password'])
    if user is None:
        await message.answer(text="Username yoki Parol xato!")
        await start_command(message, state=state)
        return

    account = account_model.get_account_by_telegram_id(message.from_user.id)
    if account is None:
        account_model.create_account(user_id=user['id'], first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name, telegram_id=message.from_user.id,
                                     telegram_username=message.from_user.username)

    else:
        if account.get('is_logout'):
            account_model.update_logout_status(message.from_user.id)

        else:
            account_model.update_account(account_id=account['id'], user_id=user[0],
                                         first_name=message.from_user.first_name,
                                         last_name=message.from_user.last_name,
                                         telegram_username=message.from_user.username)
    await message.answer(text="MP-TV botiga xush kelibsiz!")
    await start_command(message, state=state)