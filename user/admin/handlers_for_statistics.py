from datetime import timedelta

from aiogram import Router, types, F

from main import start_command
from queries.for_account import AccountModel
from queries.for_social_users import SocialUsersModel, SocialEnum
from utils.additions import tashkent_time
from utils.validator import my_validator

router_for_statistics = Router()

account_model = AccountModel()
social_users_model = SocialUsersModel()


@router_for_statistics.callback_query(F.data == "statistics_admin")
async def statistics_admin(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    data = ""
    active_accounts_on_30 = account_model.get_active_accounts_by_days(tashkent_time-timedelta(days=30), tashkent_time)
    active_accounts_on_7 = account_model.get_active_accounts_by_days(tashkent_time - timedelta(days=7), tashkent_time)
    active_accounts_on_1 = account_model.get_active_accounts_by_days(tashkent_time - timedelta(days=1), tashkent_time)

    instagram_statistics = social_users_model.get_all_social_users_by_social_media(SocialEnum.INSTAGRAM.value)
    instagram_statistics_on_30 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.INSTAGRAM.value,
        start_date=tashkent_time - timedelta(days=30),
        end_date=tashkent_time
    )
    instagram_statistics_on_7 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.INSTAGRAM.value,
        start_date=tashkent_time - timedelta(days=7),
        end_date=tashkent_time
    )
    instagram_statistics_on_1 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.INSTAGRAM.value,
        start_date=tashkent_time - timedelta(days=1),
        end_date=tashkent_time
    )

    youtube_statistics = social_users_model.get_all_social_users_by_social_media(SocialEnum.YOUTUBE.value)
    youtube_statistics_on_30 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.YOUTUBE.value,
        start_date=tashkent_time - timedelta(days=30),
        end_date=tashkent_time
    )
    youtube_statistics_on_7 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.YOUTUBE.value,
        start_date=tashkent_time - timedelta(days=7),
        end_date=tashkent_time
    )
    youtube_statistics_on_1 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.YOUTUBE.value,
        start_date=tashkent_time - timedelta(days=1),
        end_date=tashkent_time
    )

    tiktok_statistics = social_users_model.get_all_social_users_by_social_media(SocialEnum.TIKTOK.value)
    tiktok_statistics_on_30 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.TIKTOK.value,
        start_date=tashkent_time - timedelta(days=30),
        end_date=tashkent_time
    )
    tiktok_statistics_on_7 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.TIKTOK.value,
        start_date=tashkent_time - timedelta(days=7),
        end_date=tashkent_time
    )
    tiktok_statistics_on_1 = social_users_model.get_socials_by_days(
        social_media=SocialEnum.TIKTOK.value,
        start_date=tashkent_time - timedelta(days=1),
        end_date=tashkent_time
    )

    if not active_accounts_on_30:
        data += "30 Kun Ichidagi Aktiv Userlar Mavjud Emas\n"

    else:
        data += f"30 Kun Ichidagi Aktiv Userlar: {len(active_accounts_on_30)}\n"

    if not active_accounts_on_7:
        data += "7 Kun Ichidagi Aktiv Userlar Mavjud Emas\n"
    else:
        data += f"7 Kun Ichidagi Aktiv Userlar: {len(active_accounts_on_7)}\n"

    if not active_accounts_on_1:
        data += "1 Kun Ichidagi Aktiv Userlar Mavjud Emas\n\n"
    else:
        data += f"1 Kun Ichidagi Aktiv Userlar: {len(active_accounts_on_1)}\n\n"

    if not instagram_statistics:
        data += "Instagramda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"Instagramda Kelgan Userlar: {len(instagram_statistics)}"

    if not instagram_statistics_on_30:
        data += "30 Kun Ichidagi Instagramda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"30 Kun Ichidagi Instagramda Kelgan Userlar: {len(instagram_statistics_on_30)}\n"

    if not instagram_statistics_on_7:
        data += "7 Kun Ichidagi Instagramda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"7 Kun Ichidagi Instagramda Kelgan Userlar: {len(instagram_statistics_on_7)}\n"

    if not instagram_statistics_on_1:
        data += "1 Kun Ichidagi Instagramda Kelgan Userlar Mavjud Emas\n\n"
    else:
        data += f"1 Kun Ichidagi Instagramda Kelgan Userlar: {len(instagram_statistics_on_1)}\n\n"

    if not youtube_statistics:
        data += "Youtubeda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"Youtubeda Kelgan Userlar: {len(youtube_statistics)}"

    if not youtube_statistics_on_30:
        data += "30 Kun Ichidagi Youtubeda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"30 Kun Ichidagi Youtubeda Kelgan Userlar: {len(youtube_statistics_on_30)}\n"

    if not youtube_statistics_on_7:
        data += "7 Kun Ichidagi Youtubeda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"7 Kun Ichidagi Youtubeda Kelgan Userlar: {len(youtube_statistics_on_7)}\n"

    if not youtube_statistics_on_1:
        data += "1 Kun Ichidagi Youtubeda Kelgan Userlar Mavjud Emas\n\n"
    else:
        data += f"1 Kun Ichidagi Youtubeda Kelgan Userlar: {len(youtube_statistics_on_1)}\n\n"

    if not tiktok_statistics:
        data += "TikTokda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"TikTokda Kelgan Userlar: {len(tiktok_statistics)}"

    if not tiktok_statistics_on_30:
        data += "30 Kun Ichidagi TikTokda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"30 Kun Ichidagi TikTokda Kelgan Userlar: {len(tiktok_statistics_on_30)}\n"

    if not tiktok_statistics_on_7:
        data += "7 Kun Ichidagi TikTokda Kelgan Userlar Mavjud Emas\n"
    else:
        data += f"7 Kun Ichidagi TikTokda Kelgan Userlar: {len(tiktok_statistics_on_7)}\n"

    if not tiktok_statistics_on_1:
        data += "1 Kun Ichidagi TikTokda Kelgan Userlar Mavjud Emas"
    else:
        data += f"1 Kun Ichidagi TikTokda Kelgan Userlar: {len(tiktok_statistics_on_1)}"

    await call.message.answer(text=data)

    await start_command(message=call.message, user=call.from_user, delete=False)