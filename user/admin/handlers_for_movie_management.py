from datetime import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from buttons.for_admin import skip_menu, validate_menu
from queries.for_category import CategoryModel
from queries.for_company import CompanyModel
from queries.for_country import CountryModel
from queries.for_genre import GenreModel
from queries.for_language import LanguageModel
from queries.for_movie import MovieModel
from queries.for_movie_company import MovieCompanyModel
from queries.for_movie_genre import MovieGenreModel
from states.for_admin import AddMovie, DeleteMovie
from user.admin.handlers_for_admin import movies_management
from utils.validator import my_validator

router_for_movie_management = Router()

movie_model = MovieModel()
company_model = CompanyModel()
language_model = LanguageModel()
country_model = CountryModel()
category_model = CategoryModel()
genre_model = GenreModel()
movie_genre_model = MovieGenreModel()
movie_company_model = MovieCompanyModel()


@router_for_movie_management.callback_query(F.data == 'add_movie')
async def add_movie(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Film qo'shish uchun nomini kiriting:")
    await state.set_state(AddMovie.title)


@router_for_movie_management.message(AddMovie.title)
async def add_movie_title(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None:
        await message.answer("Nomi bo'sh bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    await state.update_data(title=message.text)
    await message.answer("Chiqarilgan yilini kiriting:")
    await state.set_state(AddMovie.release_date)


@router_for_movie_management.message(AddMovie.release_date)
async def add_movie_release_date(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None or not message.text.isnumeric():
        await message.answer("Chiqarilgan yili formati xato!")
        await movies_management(message=message, state=state)
        return

    current_year = datetime.now().year
    if int(message.text) > int(current_year):
        await message.answer("Chiqarilgan yili hozirgi yildan katta bo'lishi mumkin emas!")
        await movies_management(message=message, state=state)
        return

    last_code = movie_model.get_last_movie()
    if last_code:
        last_code = last_code.get('code')

    else:
        last_code = 'Mavjud Emas!'

    await state.update_data(release_date=int(message.text))
    await message.answer(f"Oxirgi Yuklangan Filmning Kodi: {last_code}"
                         "\nFilmning Kodini Kiriting:")
    await state.set_state(AddMovie.code)


@router_for_movie_management.message(AddMovie.code)
async def add_movie_code(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text is None or not message.text.isnumeric():
        await message.answer("Filmning Kod formati xato!")
        await movies_management(message=message, state=state)
        return

    movie = movie_model.get_movie_by_code(code=message.text)
    if movie is not None:
        await message.answer("Bu Kodlik film allaqachon mavjud!")
        await movies_management(message=message, state=state)
        return

    categories = category_model.get_all_categories()
    data = ''
    for category in categories:
        data += f"{category['id']}. {category['name']}\n"

    await message.answer(text=f"Kategoriyalar Ro'yxati:\n{data}")

    await state.update_data(code=message.text)
    await message.answer("Filmning Kategoriyasi ID sini kiriting:")
    await state.set_state(AddMovie.category_id)


@router_for_movie_management.message(AddMovie.category_id)
async def add_movie_category_id(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text is None or not message.text.isnumeric():
        await message.answer("Filmning Kategoriyasi ID formati xato!")
        await movies_management(message=message, state=state)
        return

    category = category_model.get_category_by_id(category_id=int(message.text))
    if category is None:
        await message.answer("Bu ID lik kategoriya topilmadi!")
        await movies_management(message=message, state=state)
        return

    companies = company_model.get_all_companies()
    data = ''
    for company in companies:
        data += f"{company['id']}. {company['name']}\n"

    await message.answer(text=f"Kompaniyalar Ro'yxati:\n{data}")

    await state.update_data(category_id=int(message.text))
    await message.answer("Filmning Companiyasini ID sini kiriting:\n"
                         ", - shu belgi bilan barchasi ajralib tursin!")
    await state.set_state(AddMovie.company_ids)


@router_for_movie_management.message(AddMovie.company_ids)
async def add_movie_company_id(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text:
        company_ids = [company_id.strip() for company_id in message.text.split(',')]
        if len(company_ids) > 0:
            try:
                for company_id in company_ids:
                    company = company_model.get_company_by_id(company_id=company_id)
                    if company is None:
                        await message.answer(f"{company_id} - Bunday ID lik companiya mavjud emas!")
                        await movies_management(message=message, state=state)
                        return

            except ValueError:
                await message.answer("Xato Narsa Kiritildi!")
                await movies_management(message=message, state=state)
                return

        else:
            await message.answer("Xato Narsa Kiritildi!")
            await movies_management(message=message, state=state)
            return

        await state.update_data(company_ids=company_ids)

    languages = language_model.get_all_languages()
    data = ''
    for language in languages:
        data += f"{language['id']}. {language['name']}\n"

    await message.answer(text=f"Tillar Ro'yxati:\n{data}")

    await message.answer("Filmning tilini ID sini kiriting:")
    await state.set_state(AddMovie.language_id)


@router_for_movie_management.message(AddMovie.language_id)
async def add_movie_language_id(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None or not message.text.isnumeric():
        await message.answer("Filmning tilini ID formati xato!")
        await movies_management(message=message, state=state)
        return

    language = language_model.get_language_by_id(language_id=int(message.text))
    if language is None:
        await message.answer("Bu ID lik til topilmadi!")
        await movies_management(message=message, state=state)
        return

    countries = country_model.get_all_countries()
    data = ''
    for country in countries:
        data += f"{country['id']}. {country['name']}\n"

    await message.answer(text=f"Davlatlar Ro'yxati:\n{data}")

    await state.update_data(language_id=int(message.text))
    await message.answer("Filmning davlatini ID sini kiriting:")
    await state.set_state(AddMovie.country_id)


@router_for_movie_management.message(AddMovie.country_id)
async def add_movie_country_id(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)
    if message.text is None or not message.text.isnumeric():
        await message.answer("Filmning davlatini ID formati xato!")
        await movies_management(message=message, state=state)
        return

    country = country_model.get_country_by_id(country_id=int(message.text))
    if country is None:
        await message.answer("Bu ID lik davlat topilmadi!")
        await movies_management(message=message, state=state)
        return

    genres = genre_model.get_all_genres()
    data = ''
    for genre in genres:
        data += f"{genre['id']}. {genre['name']}\n"

    await message.answer(text=f"Janrlar Ro'yxati:\n{data}")

    await state.update_data(country_id=int(message.text))
    await message.answer("Filmning janrlarini ID sini kiriting:\n"
                         ", - shu belgi bilan barchasi ajralib tursin!")
    await state.set_state(AddMovie.genre_ids)


@router_for_movie_management.message(AddMovie.genre_ids)
async def add_movie_genre_ids(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text:
        genre_ids = [genre_id.strip() for genre_id in message.text.split(',')]
        if len(genre_ids) > 0:
            try:
                for genre_id in genre_ids:
                    genre = genre_model.get_genre_by_id(genre_id=genre_id)
                    if genre is None:
                        await message.answer(f"{genre_id} - Bunday ID lik janr mavjud emas!")
                        await movies_management(message=message, state=state)
                        return

            except ValueError:
                await message.answer("Xato Narsa Kiritildi!")
                await movies_management(message=message, state=state)
                return

        else:
            await message.answer("Xato Narsa Kiritildi!")
            await movies_management(message=message, state=state)
            return

        await state.update_data(genre_ids=genre_ids)

    await message.answer("Filmning 360p formatdagisini yuboring:", reply_markup=skip_menu)
    await state.set_state(AddMovie.movie_id_360)


@router_for_movie_management.message(AddMovie.movie_id_360)
async def add_movie_360p(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text == 'skip':
        pass

    elif message.video:
        await state.update_data(movie_id_360=message.video.file_id, duration=message.video.duration)

    else:
        await message.answer("Xato Narsa Kiritildi!")
        await movies_management(message=message, state=state)
        return

    await message.answer("Filmning 480p formatdagisini yuboring:", reply_markup=skip_menu)
    await state.set_state(AddMovie.movie_id_480)


@router_for_movie_management.message(AddMovie.movie_id_480)
async def add_movie_480p(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text == 'skip':
        pass

    elif message.video:
        await state.update_data(movie_id_480=message.video.file_id, duration=message.video.duration)

    else:
        await message.answer("Xato Narsa Kiritildi!")
        await movies_management(message=message, state=state)
        return

    await message.answer("Filmning 720p formatdagisini yuboring:", reply_markup=skip_menu)
    await state.set_state(AddMovie.movie_id_720)


@router_for_movie_management.message(AddMovie.movie_id_720)
async def add_movie_720p(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text == 'skip':
        pass

    elif message.video:
        await state.update_data(movie_id_720=message.video.file_id, duration=message.video.duration)

    else:
        await message.answer("Xato Narsa Kiritildi!")
        await movies_management(message=message, state=state)
        return

    await message.answer("Filmning 1080p formatdagisini yuboring:", reply_markup=skip_menu)
    await state.set_state(AddMovie.movie_id_1080)


@router_for_movie_management.message(AddMovie.movie_id_1080)
async def add_movie_1080p(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    if message.text == 'skip':
        pass

    elif message.video:
        await state.update_data(movie_id_1080=message.video.file_id, duration=message.video.duration)

    else:
        await message.answer("Xato Narsa Kiritildi!", reply_markup=ReplyKeyboardRemove())
        await movies_management(message=message, state=state)
        return

    await message.answer("Film saqlanmoqda...", reply_markup=ReplyKeyboardRemove())
    movie_data = await state.get_data()
    title = movie_data.get("title")
    release_date = movie_data.get("release_date")
    duration = movie_data.get("duration")
    code = movie_data.get("code")
    category_id = movie_data.get("category_id")
    company_ids = movie_data.get("company_ids")
    language_id = movie_data.get("language_id")
    country_id = movie_data.get("country_id")
    genre_ids = movie_data.get("genre_ids")
    movie_id_360 = movie_data.get("movie_id_360")
    movie_id_480 = movie_data.get("movie_id_480")
    movie_id_720 = movie_data.get("movie_id_720")
    movie_id_1080 = movie_data.get("movie_id_1080")

    if not movie_id_360 and not movie_id_480 and not movie_id_720 and not movie_id_1080:
        await message.answer("Filmni Hachqanday Videosiz Yuklab Bo'lmaydi Qaytadan Uruning!")
        await movies_management(message=message, state=state)
        return

    duration = int(duration) // 60

    movie = movie_model.create_movie(
        title=title,
        release_date=release_date,
        duration=duration,
        code=code,
        category_id=category_id,
        language_id=language_id,
        country_id=country_id,
        movie_id_360=movie_id_360,
        movie_id_480=movie_id_480,
        movie_id_720=movie_id_720,
        movie_id_1080=movie_id_1080
    )

    genres = ''
    for genre in genre_ids:
        genre_name = genre_model.get_genre_by_id(genre)['name']
        genres += f"#{genre_name} "

    for genre_id in genre_ids:
        movie_genre_model.create_movie_genre(movie_id=movie['id'], genre_id=genre_id)

    companies = ''
    for company in company_ids:
        company_name = company_model.get_company_by_id(company)['name']
        companies += f"#{company_name} "

    for company_id in company_ids:
        movie_company_model.create_movie_company(movie_id=movie['id'], company_id=company_id)

    language_name = language_model.get_language_by_id(language_id).get('name')
    country_name = country_model.get_country_by_id(country_id).get('name')

    qualities = ''
    if movie_id_360:
        qualities += "#360p "

    if movie_id_480:
        qualities += "#480p "

    if movie_id_720:
        qualities += "#720p "

    if movie_id_1080:
        qualities += "#1080p "

    await message.answer(f"Film saqlandi! Film ID: {movie['id']}")
    await message.answer(f"#{category_model.get_category_by_id(category_id)['name']}\n"
                         f"🔎 Kodi: {code}\n"
                         f"🎥 Nomi: {title}\n"
                         f"📅 Yili: {release_date}\n"
                         f"⏳ Davomiyligi: {duration} daqiqa\n"
                         f"🎞 Studiya: {companies}\n"
                         f"{language_name[:2]} Tili: #{language_name[2:]}\n"
                         f"🌏 Davlati: #{country_name}\n"
                         f"💾 Sifati: {qualities}\n"
                         f"🎭 Janri: {genres}")
    await movies_management(message=message, state=state)


@router_for_movie_management.callback_query(F.data == "delete_movie")
async def delete_movie(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)

    await call.answer()
    await call.message.delete()
    await call.message.answer("Filmni o'chirish uchun codini kiriting:")
    await state.set_state(DeleteMovie.code)


@router_for_movie_management.message(DeleteMovie.code)
async def delete_movie_code(message: types.Message, state: FSMContext):
    await my_validator(message=message, user=message.from_user)

    movie_code = message.text
    if not movie_code.isnumeric():
        await message.answer("Kodni formati xato!")
        await movies_management(message=message, state=state)
        return

    movie = movie_model.get_movie_by_code(code=movie_code)

    if not movie:
        await message.answer("Bunday filmi topilmadi!")
        await movies_management(message=message, state=state)
        return

    await state.update_data(code=movie['id'])
    await message.answer(f"Chindanham {movie['title']} - shuni o'chirmoqchimisiz?",
                         reply_markup=validate_menu)
    await state.set_state(DeleteMovie.validate)


@router_for_movie_management.callback_query(DeleteMovie.validate)
async def delete_movie_validate(call: types.CallbackQuery, state: FSMContext):
    await my_validator(message=call.message, user=call.from_user)

    await call.answer()
    await call.message.delete()

    data = await state.get_data()
    movie_id = data.get('code')
    movie_data = movie_model.get_movie_by_id(movie_id)

    if call.data == "yes":
        movie_model.delete_movie(movie_id=movie_id)
        await call.message.answer(f"{movie_data['title']} - o'chirildi!")

    else:
        await call.message.answer("Filmi o'chirishni bekor qilindi!")

    await movies_management(call=call, state=state, delete=False)


@router_for_movie_management.callback_query(F.data == "show_all_movies")
async def show_all_movies(call: types.CallbackQuery):
    await my_validator(message=call.message, user=call.from_user)

    await call.answer()
    await call.message.delete()

    movies = movie_model.get_all_movies()

    if not movies:
        await call.message.answer("Filmlar topilmadi!")
        await movies_management(call=call, delete=False)
        return

    text = "\n".join([f"{movie['code']}. {movie['title']}" for movie in movies])
    await call.message.answer(text)
    await movies_management(call=call, delete=False)
