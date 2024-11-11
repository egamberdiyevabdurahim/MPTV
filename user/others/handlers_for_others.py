from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from main import start_command

router_for_others = Router()


@router_for_others.callback_query(F.data == 'back_to_main')
async def back_to_main(call: types.CallbackQuery, state: FSMContext, delete=True):
    await call.answer()
    await state.clear()
    await start_command(message=call.message, user=call.from_user, delete=delete)