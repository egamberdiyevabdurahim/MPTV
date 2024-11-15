import asyncio
import threading
import time

import aiohttp
from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, InputMediaVideo, ReplyKeyboardRemove

from buttons.for_admin import skip_menu
from database_config.config import TOKEN
from main import start_command
from queries.for_account import AccountModel
from states.for_admin import SendingMessageAdmin
from utils.validator import my_validator

router_for_sending_message = Router()
bot = Bot(token=TOKEN)

account_model = AccountModel()


@router_for_sending_message.callback_query(F.data == "send_message")
async def send_message_admin(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Xabarni Kiriting:\n"
                              "<b>Bu qalin matn</b>\n"
                              "<i>Bu egri matn</i>\n"
                              "<u>Bu tagi chizilgan</u>\n"
                              "<s>Bu chizib tashlangan matn</s>\n"
                              "<code>Bu kodlik matni</code>\n"
                              '<a href="https://t.me/mp_tv_uz">Bu linki bor matn</a>')
    await state.set_state(SendingMessageAdmin.message)


@router_for_sending_message.message(SendingMessageAdmin.message)
async def send_message_admin_message(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Xabarni kiriting!")
        return

    print(message.text)

    await state.update_data(message=message.text)
    await message.answer("Rasm yoki video jo'nating:\n", reply_markup=skip_menu)
    await state.set_state(SendingMessageAdmin.photo)


@router_for_sending_message.message(SendingMessageAdmin.photo)
async def send_message_admin_photo(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.photo:
        media_items = message.photo
        highest_quality_photo = media_items[-1]
        file_id = highest_quality_photo.file_id

        data = await state.get_data()
        if 'photos' in data:
            data['photos'].append(file_id)
        else:
            data['photos'] = [file_id]

        await state.update_data(photos=data['photos'])

        await message.answer("Photo added. Send another photo/video or type 'Done' when finished.")

    if message.video:
        media_items = message.video
        file_id = media_items.file_id

        data = await state.get_data()
        if 'videos' in data:
            data['videos'].append(file_id)
        else:
            data['videos'] = [file_id]

        await state.update_data(videos=data['videos'])

        await message.answer("Video added. Send another video/photo or type 'Done' when finished.")

    elif message.text and message.text.lower() == 'done':
        data = await state.get_data()
        await state.clear()

        # Retry decorator to handle server disconnections
        def retry_on_disconnect(func):
            async def wrapper(*args, **kwargs):
                retries = 3  # Retry limit
                delay = 5  # Delay between retries in seconds
                for attempt in range(retries):
                    try:
                        return await func(*args, **kwargs)
                    except aiohttp.client_exceptions.ServerDisconnectedError as e:
                        print(f"Attempt {attempt + 1}/{retries} failed: {e}. Retrying...")
                        if attempt < retries - 1:
                            time.sleep(delay)  # Wait before retrying
                        else:
                            raise e

            return wrapper

        # Function to run an async function in a separate thread
        def run_async_in_thread(async_func, *args, **kwargs):
            loop = asyncio.new_event_loop()  # Create a new event loop
            asyncio.set_event_loop(loop)  # Set the new loop as the current loop for this thread
            loop.run_until_complete(async_func(*args, **kwargs))  # Run the async function
            loop.close()  # Close the event loop after execution

        thread = threading.Thread(target=run_async_in_thread, args=(add_end, message, data))
        thread.start()
        thread.join()

    else:
        await message.answer("Please send photos/videos or 'Done' to finish.")


async def add_end(message: types.Message, data):
    message_for_sending = data.get('message')
    photos = data.get('photos', [])
    videos = data.get('videos', [])

    media_group = []
    for photo in photos:
        media_group.append(InputMediaPhoto(media=photo))
    for video in videos:
        media_group.append(InputMediaVideo(media=video))

    if media_group and message_for_sending:
        media_group[0].caption = message_for_sending
        media_group[0].parse_mode = "HTML"

    accounts = account_model.get_all_accounts()
    print(accounts)
    for account in accounts:
        print(account)
        telegram_id = account.get('telegram_id')
        try:
            await bot.send_media_group(chat_id=telegram_id, media=media_group)
            await asyncio.sleep(0.002)
        except Exception as e:
            print(f"Failed to send media to {telegram_id}: {e}")
