from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from queries.for_category import CategoryModel
from states.for_admin import AddCategory, DeleteCategory
from user.admin.handlers_for_admin import movies_management
from utils.validator import my_validator

router_for_category_management = Router()


category_model = CategoryModel()


@router_for_category_management.callback_query(F.data == "add_category")
async def add_category(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Categoriya qo'shish uchun nomini kiriting:")
    await state.set_state(AddCategory.name)


@router_for_category_management.message(AddCategory.name)
async def add_category_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    category_name = message.text.strip()
    category = category_model.get_category_by_name(category_name=category_name)
    if category is not None:
        await message.answer("Bu nomli categoriya allaqachon mavjud!")
        await movies_management(message=message, state=state)
        return

    category_model.create_category(name=category_name)
    await message.answer("Categoriya qushildi!")
    await movies_management(message=message, state=state)


@router_for_category_management.callback_query(F.data == "delete_category")
async def delete_category(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Categoriya o'chirish uchun nomini kiriting:")
    await state.set_state(DeleteCategory.name)


@router_for_category_management.message(DeleteCategory.name)
async def delete_category_name(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    category_name = message.text.strip()
    category = category_model.get_category_by_name(category_name=category_name)
    if category is None:
        await message.answer("Bu nomli categoriya topilmadi!")
        await movies_management(message=message, state=state)
        return

    category_model.delete_category(category_id=category['id'])
    await message.answer("Categoriya o'chirildi!")
    await movies_management(message=message, state=state)


@router_for_category_management.callback_query(F.data == "show_all_categories")
async def show_all_companies(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()

    categories = category_model.get_all_categories()
    if not categories:
        await call.message.answer("Categoriyalar topilmadi!")
        await movies_management(call=call, delete=False)
        return

    text = "\n".join([f"{category['id']}. {category['name']}" for category in categories])
    await call.message.answer(text)
    await movies_management(call=call, delete=False)