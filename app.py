import logging
logging.basicConfig(level=logging.INFO)

import asyncio
import schedule
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from auth.login import login_router
from auth.register import register_router
from database_config.config import TOKEN
from main import router

from queries.for_account import AccountModel
from queries.for_running import if_not_used
from queries.for_user import UserModel
from user.admin.handlers_for_admin import router_for_admin
from user.admin.handlers_for_category_management import router_for_category_management
from user.admin.handlers_for_company_management import router_for_company_management
from user.admin.handlers_for_country_management import router_for_country_management
from user.admin.handlers_for_genre_management import router_for_genre_management
from user.admin.handlers_for_language_management import router_for_language_management
from user.admin.handlers_for_movie_management import router_for_movie_management
from user.admin.handlers_for_movies_management import router_for_movies_management
from user.admin.handlers_for_user_management import router_for_user_management
from user.others.handlers_for_others import router_for_others
from user.user.handlers_for_filtering_category import router_for_filtering_category
from user.user.handlers_for_filtering_company import router_for_filtering_company
from user.user.handlers_for_filtering_country import router_for_filtering_country
from user.user.handlers_for_filtering_genre import router_for_filtering_genre
from user.user.handlers_for_filtering_language import router_for_filtering_language
from user.user.handlers_for_filtering_likes import router_for_filtering_likes
from user.user.handlers_for_filtering_views import router_for_filtering_views
from user.user.handlers_for_filtering_year import router_for_filtering_year
from user.user.handlers_for_finding import router_for_finding
from user.user.handlers_for_finding_by_title import router_for_finding_by_title
from user.user.handlers_for_like import router_for_like
from user.user.handlers_for_profile import router_for_profile
from user.user.handlers_for_saved import router_for_saved
from user.user.handlers_for_user import router_for_user
from user.user.handlers_for_user_movie import router_for_user_movie
from utils.database_dumper import dump_and_send

account_model = AccountModel()
user_model = UserModel()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

COMMANDS = ['/start']

@dp.message(Command('support', 'help'))
async def support_command(message: types.Message):
    await message.answer(f"Yordam va Xatolar Uchun:\n"
                         "@MasterPhoneAdmin✅")

# Task to run pending schedule jobs
async def schedule_task_for_inactivate():
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # Poll every second to check schedule

async def main():
    if_not_used()
    dp.include_routers(
        router,
        login_router,
        register_router,
        router_for_others,
        router_for_admin,
        router_for_user_management,
        router_for_movies_management,
        router_for_movie_management,
        router_for_company_management,
        router_for_country_management,
        router_for_genre_management,
        router_for_language_management,
        router_for_category_management,
        router_for_user,
        router_for_finding,
        router_for_saved,
        router_for_like,
        router_for_user_movie,
        router_for_filtering_company,
        router_for_filtering_category,
        router_for_filtering_country,
        router_for_filtering_genre,
        router_for_filtering_language,
        router_for_filtering_year,
        router_for_finding_by_title,
        router_for_filtering_likes,
        router_for_filtering_views,
        router_for_profile
    )
    await dp.start_polling(bot)

async def init():
    # Schedule the task using an async lambda to avoid blocking
    schedule.every().day.at("19:12").do(lambda: asyncio.create_task(dump_and_send()))

    # Run polling and schedule task concurrently
    await asyncio.gather(main(), schedule_task_for_inactivate())

if __name__ == '__main__':
    try:
        asyncio.run(init())  # Start the async event loop
    except Exception as e:
        logging.error(f"Error starting bot: {e}")
