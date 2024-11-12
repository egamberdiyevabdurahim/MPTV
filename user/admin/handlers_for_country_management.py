from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from queries.for_country import CountryModel
from states.for_admin import AddCountry, DeleteCountry
from user.admin.handlers_for_admin import movies_management
from utils.validator import my_validator

router_for_country_management = Router()

country_model = CountryModel()


@router_for_country_management.callback_query(F.data == "add_country")
async def add_country(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Davlat qo'shish uchun nomini kiriting:")
    await state.set_state(AddCountry.name)


@router_for_country_management.message(AddCountry.name)
async def add_country_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    country_name = message.text.strip()
    country = country_model.get_country_by_name(country_name=country_name)
    if country is not None:
        await message.answer("Bu nomli davlat allaqachon mavjud!")
        await movies_management(message=message, state=state)
        return

    country_model.create_country(name=country_name)
    await message.answer("Davlat qushildi!")
    await movies_management(message=message, state=state)


@router_for_country_management.callback_query(F.data == "delete_country")
async def delete_country(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Davlat o'chirish uchun nomini kiriting:")
    await state.set_state(DeleteCountry.name)


@router_for_country_management.message(DeleteCountry.name)
async def delete_country_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    country_name = message.text.strip()
    country = country_model.get_country_by_name(country_name=country_name)
    if country is None:
        await message.answer("Bu nomli davlat topilmadi!")
        await movies_management(message=message, state=state)
        return

    country_model.delete_country(country_id=country['id'])
    await message.answer("Davlat o'chirildi!")
    await movies_management(message=message, state=state)


@router_for_country_management.callback_query(F.data == "show_all_countries")
async def show_all_countries(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()

    countries = country_model.get_all_countries()
    if not countries:
        await call.message.answer("Davlat topilmadi!")
        await movies_management(call=call, delete=False)
        return

    text = "\n".join([f"{company['id']}. {company['name']}" for company in countries])
    await call.message.answer(text)
    await movies_management(call=call, delete=False)