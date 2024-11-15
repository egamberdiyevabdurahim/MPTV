from datetime import datetime, timedelta

from aiogram import types, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from buttons.for_admin import main_menu_admin
from buttons.for_user import main_menu_auth, main_menu_un_auth
from database_config.config import TOKEN, GROUP_ID
from queries.for_account import AccountModel
from queries.for_social_users import SocialEnum, SocialUsersModel
from queries.for_user import UserModel
from utils.additions import ADMIN_LINK, ADMIN_EMAIL
from utils.for_circular import circular1

router = Router()
bot = Bot(token=TOKEN)

account_model = AccountModel()
user_model = UserModel()


@router.message(CommandStart())
async def start_command(message: types.Message, user=None, state: FSMContext = None, delete=True):
    if not user:
        user = message.from_user
    account = account_model.get_account_by_telegram_id(user.id)
    if state:
        await state.clear()

    if delete:
        await message.delete()

    if message.text:
        hidden_code = message.text.split(' ')[-1]
        if len(list(message.text.split(' '))) > 1:
            if hidden_code == SocialEnum.INSTAGRAM.value:
                if not account:
                    user_id = account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                    SocialUsersModel().create_social_user(user_id=user_id, social_media=SocialEnum.INSTAGRAM.value)

            elif hidden_code == SocialEnum.TIKTOK.value:
                if not account:
                    user_id = account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                    SocialUsersModel().create_social_user(user_id=user_id, social_media=SocialEnum.TIKTOK.value)

            elif hidden_code == SocialEnum.YOUTUBE.value:
                if not account:
                    user_id = account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                    SocialUsersModel().create_social_user(user_id=user_id, social_media=SocialEnum.YOUTUBE.value)

            elif message.text.split(' ')[1] == SocialEnum.INSTAGRAM.value and hidden_code.isnumeric():
                if not account:
                    user_id = account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                    SocialUsersModel().create_social_user(user_id=user_id, social_media=SocialEnum.INSTAGRAM.value)
                await circular1(message, state, hidden_code)

            elif message.text.split(' ')[1] == SocialEnum.TIKTOK.value and hidden_code.isnumeric():
                if not account:
                    user_id = account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                    SocialUsersModel().create_social_user(user_id=user_id, social_media=SocialEnum.TIKTOK.value)
                await circular1(message, state, hidden_code)

            elif message.text.split(' ')[1] == SocialEnum.YOUTUBE.value and hidden_code.isnumeric():
                if not account:
                    user_id = account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                    SocialUsersModel().create_social_user(user_id=user_id, social_media=SocialEnum.YOUTUBE.value)
                await circular1(message, state, hidden_code)

            elif hidden_code.isnumeric():
                if not account:
                    account_model.create_account(
                        first_name=user.first_name,
                        telegram_id=user.id,
                        last_name=user.last_name,
                        telegram_username=user.username
                    )
                await circular1(message, state, hidden_code)

    # Check if user is registered
    user = user if user else message.from_user
    is_auth = account_model.is_account_registered(telegram_id=user.id)

    # Send welcome message with appropriate menu
    if is_auth:
        await message.answer(
            f"Assalamu Aleykum\n{user.first_name}, Botimizga Xush Kelibsiz😊!\n\n"
            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support",

            protect_content=True,
            reply_markup=main_menu_admin
            if user_model.get_user_by_id(
                account_model.get_account_by_telegram_id(user.id)['user_id']).get('is_admin') else main_menu_auth
        )

    else:
        await message.answer(
            f"Assalamu Aleykum\n{user.first_name}, Botimizga Xush Kelibsiz😊!\n\n"
            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support",

            protect_content=True,
            reply_markup=main_menu_un_auth)

        if account is not None:
            account_model.add_used(account['id'])

        else:
            # await bot.send_message(chat_id=GROUP_ID, text=f"Yangi Botga start bergan foydalanuvchi:"
            #                                               f"Ismi: {user.first_name}\n"
            #                                               f"Familiyasi: {user.last_name if user.last_name else 'Mavjud Emasta'}\n"
            #                                               f"Telegram ID: {user.id}\n"
            #                                               f"Telegram Username: {user.username if user.username else 'Mavjud Emas'}")
            account_model.create_account(
                first_name=user.first_name,
                telegram_id=user.id,
                last_name=user.last_name,
                telegram_username=user.username
            )


@router.message(Command('statistics'))
async def statistics_command(message: types.Message):
    total_accounts = len(account_model.get_all_accounts())
    total_accounts_in_month = len(account_model.get_all_accounts_by_days(
        start_date=datetime.now()-timedelta(days=30),
        end_date=datetime.now()
    ))
    text_data = (f"MP TV botimizda 1 oy ichida yangi qo'shilganlar soni: {total_accounts_in_month}\n"
                 f"MP TV botimizdagi umumiy foydalanuvchilar soni: {total_accounts}")
    await message.answer(text=text_data)


@router.message(Command("dev"))
async def dev_command(message: types.Message):
    await message.answer(f"""
🖥 Dasturchi haqida 🖥
    
Ushbu Telegram botni yasagan {ADMIN_LINK} — tajribali va malakali dasturchi.
U har qanday murakkab dasturiy loyihalarni yaratish va texnik yechimlarni taklif etishda keng tajribaga ega.
    
{ADMIN_LINK} dasturchi, sizga quyidagi xizmatlarni taklif qiladi:

Telegram botlar (maxsus, avtomatlashtirilgan tizimlar)
Veb ilovalar va saytlar
Mobil ilovalar
Maxsus dasturiy yechimlar va tizimlar
API integratsiyalari

💼 Xizmatlar:

Telegram botlar va kanal boshqaruvi
Veb ilovalar va saytlar ishlab chiqish
Mobil ilovalar yaratish
Dasturiy integratsiyalar va maxsus yechimlar

📞 Bog‘lanish uchun:

Telegram: {ADMIN_LINK}
Email: {ADMIN_EMAIL}
GitHub: github.com/egamberdiyevabdurahim
🔧 Loyihangizni mukammal qilish uchun yordam berishga tayyorman!
""")