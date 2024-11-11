from aiogram import types, Bot

from database_config.config import TOKEN
from queries.for_account import AccountModel

bot = Bot(token=TOKEN)


async def message_deleter(message: types.Message, user):
    try:
        await bot.delete_message(message_id=message.message_id-1, chat_id=user.id)
        await message.delete()

    except Exception:
        pass


async def my_validator(message: types.Message, user, delete_message=None):
    account_model = AccountModel()
    account = account_model.get_account_by_telegram_id(user.id)
    account_model.add_used(account['id'])
    # await message.delete()
    if delete_message:
        await message_deleter(message, user)
