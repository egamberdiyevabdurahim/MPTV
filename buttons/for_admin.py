from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

main_menu_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Profil", callback_data="profile"), InlineKeyboardButton(text="Admin", callback_data="admin")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Kodi orqali topish", callback_data="movie_from_code")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Izlash", callback_data="movie_find")],
])


admin_panel_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Userlar Boshqaruvi", callback_data="user_management")],
    [InlineKeyboardButton(text="Kino yoki Multfilm Boshqaruvi(Asosiy)", callback_data="movies_management")],
    [InlineKeyboardButton(text="Statistics", callback_data="statistics_admin")],
    [InlineKeyboardButton(text="Xabar Jo'natiash", callback_data="send_message")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_main")],
])


user_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    # [InlineKeyboardButton(text="Userni Bloklash", callback_data="delete_user")],
    [InlineKeyboardButton(text="Barcha Userlarni Ko'rish", callback_data='show_all_users')],
    [InlineKeyboardButton(text="Barcha Akkauntlarni Ko'rish", callback_data='show_all_accounts')],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_admin")],
])


movies_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Kino yoki Multfilm Boshqaruvi", callback_data="movie_management")],
    [InlineKeyboardButton(text="Kompaniya Boshqaruvi", callback_data="company_management"),
     InlineKeyboardButton(text="Davlat Boshqaruvi", callback_data="country_management")],
    [InlineKeyboardButton(text="Janr Boshqaruvi", callback_data="genre_management"),
     InlineKeyboardButton(text="Til Boshqaruvi", callback_data="language_management")],
    [InlineKeyboardButton(text="Categoriya Boshqaruvi", callback_data="category_management")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_admin")],
])


movie_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Kino yoki Multfilm qo'shish", callback_data="add_movie")],
    [InlineKeyboardButton(text="Kino yoki Multfilm o'chirish", callback_data="delete_movie")],
    [InlineKeyboardButton(text="Barcha Kino yoki Multfilmlarni Ko'rish", callback_data="show_all_movies")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_movies")],
])


company_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Kompaniya qo'shish", callback_data="add_company")],
    [InlineKeyboardButton(text="Kompaniya o'chirish", callback_data="delete_company")],
    [InlineKeyboardButton(text="Barcha Kompaniyalarni Ko'rish", callback_data="show_all_companies")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_movies")],
])


country_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Davlat qo'shish", callback_data="add_country")],
    [InlineKeyboardButton(text="Davlat o'chirish", callback_data="delete_country")],
    [InlineKeyboardButton(text="Barcha Davlatlarni Ko'rish", callback_data="show_all_countries")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_movies")],
])


genre_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Janr qo'shish", callback_data="add_genre")],
    [InlineKeyboardButton(text="Janr o'chirish", callback_data="delete_genre")],
    [InlineKeyboardButton(text="Barcha Janrlarni Ko'rish", callback_data="show_all_genres")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_movies")],
])


language_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Til qo'shish", callback_data="add_language")],
    [InlineKeyboardButton(text="Til o'chirish", callback_data="delete_language")],
    [InlineKeyboardButton(text="Barcha Tillarni Ko'rish", callback_data="show_all_languages")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_movies")],
])


category_management_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Categoriya qo'shish", callback_data="add_category")],
    [InlineKeyboardButton(text="Categoriya o'chirish", callback_data="delete_category")],
    [InlineKeyboardButton(text="Barcha Categoriyalarni Ko'rish", callback_data="show_all_categories")],
    [InlineKeyboardButton(text="Ortga", callback_data="back_to_movies")],
])


skip_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="skip")],],
    resize_keyboard=True,
    one_time_keyboard=True,
    is_persistent=True,
)


validate_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Ha", callback_data="yes")],
    [InlineKeyboardButton(text="Yo'q", callback_data="no")],
])