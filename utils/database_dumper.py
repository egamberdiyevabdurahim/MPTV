import os
import subprocess
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile

from database_config.config import GROUP_ID, DB_USER, DB_NAME, TOKEN, DB_HOST, DB_PORT, DB_PASS
from utils.additions import BASE_PATH, tashkent_time

DUMP_PATH = f'{BASE_PATH}/database.sql'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

async def send_dump_to_telegram():
    if os.path.exists(DUMP_PATH):
        document = FSInputFile(DUMP_PATH)
        try:
            await bot.send_document(chat_id=GROUP_ID, document=document,
                                    caption=tashkent_time.strftime("%Y-%m-%d %H:%M"))
        except Exception as e:
            await bot.send_message(text=f"Error sending file: {str(e)}", chat_id=GROUP_ID)

        os.remove(DUMP_PATH)
    else:
        await bot.send_message(text=f"Error sending file .sql", chat_id=GROUP_ID)


async def dump_and_send():
    try:
        dump_command = f"pg_dump -U {DB_USER} -h {DB_HOST} -p {DB_PORT} -F c -d {DB_NAME} -f {DUMP_PATH}"
        env = os.environ.copy()  # Copy the environment variables
        env['PGPASSWORD'] = DB_PASS  # Set the password for pg_dump
        subprocess.run(dump_command, shell=True, check=True, env=env)

        await send_dump_to_telegram()

    except subprocess.CalledProcessError as e:
        await bot.send_message(text=f"Error dumping or compressing the database: {e}", chat_id=GROUP_ID)
