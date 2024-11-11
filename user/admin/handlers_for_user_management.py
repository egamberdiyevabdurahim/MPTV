import os

from aiogram import Router, types, F
from aiogram.types import FSInputFile

from buttons.for_user import back_button
from queries.for_account import AccountModel
from queries.for_user import UserModel
from utils.additions import BASE_PATH

router_for_user_management = Router()

user_model = UserModel()
account_model = AccountModel()


@router_for_user_management.callback_query(F.data == 'show_all_users')
async def show_all_users(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    user_file_path = os.path.join(BASE_PATH, "users.txt")

    users = user_model.get_all_users()
    with open(user_file_path, "w") as f:
        for user in users:
            user_data = (f"ID: {user['id']}\n"
                         f"Username: {user['username']}\n"
                         f"Password: {user['password']}\n")
            for account in account_model.get_accounts_by_user_id(user_id=user['id']):
                last_name = account['last_name'] or "Mavjud Emas"
                user_data += (f"\n    ID: {account['id']}\n"
                              f"    Telegram ID: {account['telegram_id']}\n"
                              f"    First Name: {account['first_name']}\n"
                              f"    Last Name: {last_name}\n"
                              f"    Telegram Username: @{account['telegram_username']}\n"
                              f"    Used: {account['used']}\n"
                              f"    Created At: {user['created_at']}\n"
                              f"    Updated At: {user['updated_at']}\n"
                              f"    {'-' * 20}\n")

            user_data += f"{'&' * 25}"
            f.write(user_data)

    if os.path.exists(user_file_path):
        file = FSInputFile(user_file_path)
        await call.message.answer_document(document=file, reply_markup=back_button)
        os.remove(user_file_path)
