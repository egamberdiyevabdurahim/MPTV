from datetime import datetime, timedelta

from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from buttons.for_admin import main_menu_admin
from buttons.for_user import main_menu_auth, main_menu_un_auth
from queries.for_account import AccountModel
from queries.for_user import UserModel

router = Router()

account_model = AccountModel()
user_model = UserModel()


@router.message(CommandStart())
async def start_command(message: types.Message, user=None, state: FSMContext = None, delete=True):
    # Clear state if provided
    await state.clear()

    if delete:
        await message.delete()

    # Check if user is registered
    user = user if user else message.from_user
    is_auth = account_model.is_account_registered(telegram_id=user.id)

    # Send welcome message with appropriate menu
    if is_auth:
        await message.answer(
            f"Assalamu Aleykum\n{user.first_name}, Botimizga Xush Kelibsiz😊!\n\n"
            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support",

            protect_content=True,
            reply_markup=main_menu_admin
            if user_model.get_user_by_id(
                account_model.get_account_by_telegram_id(user.id)['user_id']).get('is_admin') else main_menu_auth
        )

    else:
        await message.answer(
            f"Assalamu Aleykum\n{user.first_name}, Botimizga Xush Kelibsiz😊!\n\n"
            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support",

            protect_content=True,
            reply_markup=main_menu_un_auth)

        account = account_model.get_account_by_telegram_id(user.id)
        if account is not None:
            account_model.add_used(account['id'])

        else:
            account_model.create_account(
                first_name=user.first_name,
                telegram_id=user.id,
                last_name=user.last_name,
                telegram_username=user.username
            )


@router.message(Command('statistics'))
async def statistics_command(message: types.Message):
    total_accounts = len(account_model.get_all_accounts())
    total_accounts_in_month = len(account_model.get_all_accounts_by_days(
        start_date=datetime.now()-timedelta(days=30),
        end_date=datetime.now()
    ))
    text_data = (f"MP TV botimizda 1 oy ichida yangi qo'shilganlar soni: {total_accounts_in_month}\n"
                 f"MP TV botimizdagi umumiy foydalanuvchilar soni: {total_accounts}")
    await message.answer(text=text_data)