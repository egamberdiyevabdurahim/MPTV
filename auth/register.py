from aiogram import types, F, Router
from aiogram.fsm.context import FSMContext

from main import start_command
from buttons.for_user import back_button

from queries.for_account import AccountModel
from queries.for_user import UserModel

from states.for_auth import RegisterState
from utils.validator import my_validator

account_model = AccountModel()
user_model = UserModel()

register_router = Router()


@register_router.callback_query(F.data == "register")
async def register1(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer(text="Username kiriting:", reply_markup=back_button)
    await state.set_state(RegisterState.username)


@register_router.message(RegisterState.username)
async def register2(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer(text="Username bo'sh bo'lishi mumkin emas!")
        await start_command(message, state=state)
        return

    user = user_model.get_user_by_username(username=message.text.lower().strip())
    if user is not None:
        await message.answer(text="Bu username allaqachon mavjud!")
        await start_command(message, state=state)
        return

    await state.update_data(username=message.text.lower().strip())
    await message.answer(text="Parol kiriting:", reply_markup=back_button)
    await state.set_state(RegisterState.password)


@register_router.message(RegisterState.password)
async def register3(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer(text="Parol bo'sh bo'lishi mumkin emas!")
        await start_command(message, state=state)
        return

    state_data = await state.get_data()

    user = user_model.create_user(username=state_data['username'], password=message.text.strip())
    account = account_model.get_account_by_telegram_id(message.from_user.id)
    if account is None:
        account_model.create_account(user_id=user['id'], first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name, telegram_id=message.from_user.id,
                                     telegram_username=message.from_user.username)

    else:
        account_model.update_account(account_id=account['id'], user_id=user['id'],
                                     first_name=message.from_user.first_name,
                                     last_name=message.from_user.last_name,
                                     telegram_username=message.from_user.username)

    await message.answer(text="MP-Video botiga xush kelibsiz!")
    await start_command(message, state=state)
