from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from main import start_command
from queries.for_genre import GenreModel
from states.for_admin import AddGenre, DeleteGenre
from user.admin.handlers_for_admin import movies_management
from utils.validator import my_validator

router_for_genre_management = Router()

genre_model = GenreModel()


@router_for_genre_management.callback_query(F.data == "add_genre")
async def add_genre(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Janr qo'shish uchun nomini kiriting:")
    await state.set_state(AddGenre.name)


@router_for_genre_management.message(AddGenre.name)
async def add_genre_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    genre_name = message.text.strip()
    genre = genre_model.get_genre_by_name(genre_name=genre_name)
    if genre is not None:
        await message.answer("Bu nomli janr allaqachon mavjud!")
        await movies_management(message=message, state=state)
        return

    genre_model.create_genre(name=genre_name)
    await message.answer("Janr qushildi!")
    await state.clear()
    await start_command(message, user=message.from_user)


@router_for_genre_management.callback_query(F.data == "delete_genre")
async def delete_genre(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Janr o'chirish uchun nomini kiriting:")
    await state.set_state(DeleteGenre.name)


@router_for_genre_management.message(DeleteGenre.name)
async def delete_genre_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    genre_name = message.text.strip()
    genre = genre_model.get_genre_by_name(genre_name=genre_name)
    if genre is None:
        await message.answer("Bu nomli janr topilmadi!")
        await movies_management(message=message, state=state)
        return

    genre_model.delete_genre(genre_id=genre['id'])
    await message.answer("Janr o'chirildi!")
    await state.clear()
    await start_command(message, user=message.from_user)


@router_for_genre_management.callback_query(F.data == "show_all_genres")
async def show_all_genre(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()

    genre = genre_model.get_all_genres()
    if not genre:
        await call.message.answer("Janr topilmadi!")
        await movies_management(call=call, delete=False)
        return

    text = "\n".join([f"{company['id']}. {company['name']}" for company in genre])
    await call.message.answer(text)
    await movies_management(call=call, delete=False)