from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from queries.for_company import CompanyModel
from states.for_admin import AddCompany, DeleteCompany
from user.admin.handlers_for_admin import movies_management
from utils.validator import my_validator

router_for_company_management = Router()


company_model = CompanyModel()


@router_for_company_management.callback_query(F.data == "add_company")
async def add_company(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Kompaniya qo'shish uchun nomini kiriting:")
    await state.set_state(AddCompany.name)


@router_for_company_management.message(AddCompany.name)
async def add_company_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    company_name = message.text.strip()
    company = company_model.get_company_by_name(company_name=company_name)
    if company is not None:
        await message.answer("Bu nomli kompaniya allaqachon mavjud!")
        await movies_management(message=message, state=state)
        return

    company_model.create_company(name=company_name)
    await message.answer("Kompaniya qushildi!")
    await state.clear()
    await movies_management(message=message, state=state)


@router_for_company_management.callback_query(F.data == "delete_company")
async def delete_company(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Kompaniya o'chirish uchun nomini kiriting:")
    await state.set_state(DeleteCompany.name)


@router_for_company_management.message(DeleteCompany.name)
async def delete_company_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    company_name = message.text.strip()
    company = company_model.get_company_by_name(company_name=company_name)
    if company is None:
        await message.answer("Bu nomli kompaniya topilmadi!")
        await movies_management(message=message, state=state)
        return

    company_model.delete_company(company_id=company['id'])
    await message.answer("Kompaniya o'chirildi!")
    await state.clear()
    await movies_management(message=message, state=state)


@router_for_company_management.callback_query(F.data == "show_all_companies")
async def show_all_companies(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()

    companies = company_model.get_all_companies()
    if not companies:
        await call.message.answer("Kompaniyalar topilmadi!")
        await movies_management(call=call, delete=False)
        return

    text = "\n".join([f"{company['id']}. {company['name']}" for company in companies])
    await call.message.answer(text)
    await movies_management(call=call, delete=False)