from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from main import start_command
from queries.for_language import LanguageModel
from states.for_admin import AddLanguage, DeleteLanguage
from user.admin.handlers_for_admin import movies_management
from utils.validator import my_validator

router_for_language_management = Router()

language_model = LanguageModel()


@router_for_language_management.callback_query(F.data == "add_language")
async def add_language(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Til qo'shish uchun nomini kiriting:")
    await state.set_state(AddLanguage.name)


@router_for_language_management.message(AddLanguage.name)
async def add_language_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    language_name = message.text.strip()
    language = language_model.get_language_by_name(language_name=language_name)
    if language is not None:
        await message.answer("Bu nomli til allaqachon mavjud!")
        await movies_management(message=message, state=state)
        return

    language_model.create_language(name=language_name)
    await message.answer("Til qushildi!")
    await movies_management(message=message, state=state)


@router_for_language_management.callback_query(F.data == "delete_language")
async def delete_language(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Til o'chirish uchun nomini kiriting:")
    await state.set_state(DeleteLanguage.name)


@router_for_language_management.message(DeleteLanguage.name)
async def delete_language_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    language_name = message.text.strip()
    language = language_model.get_language_by_name(language_name=language_name)
    if language is None:
        await message.answer("Bu nomli til topilmadi!")
        await movies_management(message=message, state=state)
        return

    language_model.delete_language(language_id=language['id'])
    await message.answer("Til o'chirildi!")
    await movies_management(message=message, state=state)


@router_for_language_management.callback_query(F.data == "show_all_languages")
async def show_all_languages(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()

    languages = language_model.get_all_languages()
    if not languages:
        await call.message.answer("Til topilmadi!")
        await movies_management(call=call, delete=False)
        return

    text = "\n".join([f"{company['id']}. {company['name']}" for company in languages])
    await call.message.answer(text)
    await movies_management(call=call, delete=False)