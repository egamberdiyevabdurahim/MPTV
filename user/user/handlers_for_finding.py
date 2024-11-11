from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from buttons.for_user import quality_movie_menu, watch_movie_menu, back_button
from queries.for_account import AccountModel
from queries.for_category import CategoryModel
from queries.for_company import CompanyModel
from queries.for_country import CountryModel
from queries.for_genre import GenreModel
from queries.for_language import LanguageModel
from queries.for_movie import MovieModel
from queries.for_movie_company import MovieCompanyModel
from queries.for_movie_genre import MovieGenreModel
from queries.for_user import UserModel
from states.for_user import MovieFromCodeState
from user.others.handlers_for_others import back_to_main

router_for_finding = Router()

account_model = AccountModel()
user_model = UserModel()
movie_model = MovieModel()
category_model = CategoryModel()
country_model = CountryModel()
language_model = LanguageModel()
genre_model = GenreModel()
company_model = CompanyModel()
movie_genre_model = MovieGenreModel()
movie_company_model = MovieCompanyModel()


@router_for_finding.callback_query(F.data == "movie_from_code")
async def movie_from_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer("Kino kodini kiriting:", reply_markup=back_button)
    await state.set_state(MovieFromCodeState.code)


@router_for_finding.message(MovieFromCodeState.code)
async def movie_from_code_code(message: types.Message, state: FSMContext):
    if message.text is None:
        await message.answer("Kod formati xato!", reply_markup=back_button)
        return

    if not message.text.isnumeric():
        await message.answer("Kod formati xato!", reply_markup=back_button)
        return

    movie_code = message.text.strip()
    movie = movie_model.get_movie_by_code(code=movie_code)
    if movie is None:
        await message.answer("Bunday kino topilmadi!", reply_markup=back_button)
        return

    await state.update_data(code=movie['id'])
    await message.answer("Sifatini Tanlang:", reply_markup=await quality_movie_menu(movie))
    await state.set_state(MovieFromCodeState.quality)


@router_for_finding.callback_query(F.data.startswith("movie_filtering_"))
async def movie_filtering_from_id(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    movie_id = call.data.split('_')[-1]
    movie = movie_model.get_movie_by_id(movie_id)
    await state.update_data(code=movie_id, from_callback=True)
    await call.message.answer("Sifatini Tanlang:", reply_markup=await quality_movie_menu(movie))
    await state.set_state(MovieFromCodeState.quality)


@router_for_finding.callback_query(MovieFromCodeState.quality)
async def movie_from_code_quality(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.answer()
        await call.message.delete()
    except Exception:
        pass
    quality = call.data

    state_data = await state.get_data()
    movie_id = state_data['code']
    movie = movie_model.get_movie_by_id(movie_id)

    account = account_model.get_account_by_telegram_id(call.from_user.id)
    user = user_model.get_user_by_id(account['user_id'])

    movie_id = movie.get('id')
    title = movie.get('title')
    code = movie.get('code')
    release_date = movie.get('release_date')
    duration = movie.get('duration')
    category_id = movie.get('category_id')
    language_id = movie.get('language_id')
    country_id = movie.get('country_id')
    movie_id_360 = movie.get('movie_id_360')
    movie_id_480 = movie.get('movie_id_480')
    movie_id_720 = movie.get('movie_id_720')
    movie_id_1080 = movie.get('movie_id_1080')
    views_count = movie.get('views')

    # Determine the video file ID based on the quality selected
    video_quality = {
        '360': movie_id_360,
        '480': movie_id_480,
        '720': movie_id_720,
        '1080': movie_id_1080
    }.get(quality)

    # If video_quality is None, send an error message
    if video_quality is None:
        await call.message.answer("Kechirasiz, ushbu sifatda video mavjud emas.", reply_markup=back_button)
        return

    genre_ids = movie_genre_model.get_all_genres_by_movie_id(movie_id)
    genre_ids = [gen['genre_id'] for gen in genre_ids]

    company_ids = movie_company_model.get_all_companies_by_movie_id(movie_id)
    company_ids = [comp['company_id'] for comp in company_ids]

    genres = ''.join(f"#{genre_model.get_genre_by_id(genre)['name']} " for genre in genre_ids)
    companies = ''.join(f"#{company_model.get_company_by_id(company)['name']} " for company in company_ids)
    language_name = language_model.get_language_by_id(language_id).get('name')
    country_name = country_model.get_country_by_id(country_id).get('name')

    # Send the video with caption
    movie_model.add_view_count(movie_id=movie_id)
    await call.message.answer_video(
        video=video_quality,
        caption=(f"#{category_model.get_category_by_id(category_id)['name']}\n"
                 f"🔎 Kodi: {code}\n"
                 f"🎥 Nomi: {title}\n"
                 f"📅 Yili: {release_date}\n"
                 f"⏳ Davomiyligi: {duration} daqiqa\n"
                 f"🎞 Studiya: {companies}\n"
                 f"{language_name[:2]} Tili: #{language_name[2:]}\n"
                 f"🌏 Davlati: #{country_name}\n"
                 f"💾 Sifati: #{quality}p\n"
                 f"🎭 Janri: {genres}\n"
                 f"👁‍ Ko'rilgan: {views_count} | ❤️ Yoqtirilganlar: {movie_model.get_likes_count(movie_id=movie_id)}"),
        parse_mode="HTML",
        reply_markup=await watch_movie_menu(
            user_id=user.get('id') if user else None,
            movie_id=movie_id,
        )
    )
    await state.clear()
    if not state_data.get("from_callback"):
        await back_to_main(call=call, state=state, delete=False)