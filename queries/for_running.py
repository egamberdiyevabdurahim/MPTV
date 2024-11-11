from database_config.db_settings import execute_query
from queries.for_category import CategoryModel
from queries.for_movie_company import MovieCompanyModel

from queries.for_user import UserModel
from queries.for_account import AccountModel

from queries.for_company import CompanyModel
from queries.for_country import CountryModel
from queries.for_genre import GenreModel
from queries.for_hidden_history import HiddenHistoryModel
from queries.for_language import LanguageModel

from queries.for_movie import MovieModel
from queries.for_movie_genre import MovieGenreModel
from queries.for_movie_history import MovieHistoryModel
from queries.for_like import LikeModel
from queries.for_saved import SavedModel
from queries.for_user_movie import UserMovieModel


def create_is_used_table_query() -> None:
    """
    Creates a new table for tracking whether the application is already run.
    """
    query = """
        CREATE TABLE IF NOT EXISTS is_used (
            id BIGSERIAL PRIMARY KEY,
            is_used BOOLEAN DEFAULT FALSE
        );
    """
    execute_query(query)
    return None


def insert_is_used_query():
    """
    Inserts a new record into the is_used table.
    """
    query = """
        SELECT * FROM is_used
        ORDER BY id DESC
        LIMIT 1;
        """
    data = execute_query(query, fetch="one")
    if data is None:
        query = "INSERT INTO is_used (is_used) VALUES (False);"
        execute_query(query)
    return None


def update_is_used_query():
    """
    Updates the is_used column in the is_used table.
    """
    query = "UPDATE is_used SET is_used = TRUE;"
    execute_query(query)
    return None


def is_used():
    query = """
    SELECT * FROM is_used
    ORDER BY id
    LIMIT 1;
    """
    data = execute_query(query, fetch="one")
    return data['is_used'] is True


def before_run() -> None:
    """
    Creates all required tables before running the application.
    """
    # Create models
    UserModel().create_user_table()
    AccountModel().create_account_table()
    CompanyModel().create_company_table()
    CountryModel().create_country_table()
    GenreModel().create_genre_table()
    CategoryModel().create_category_table()
    HiddenHistoryModel().create_hidden_history_table()
    LanguageModel().create_language_table()
    MovieModel().create_movie_table()
    MovieGenreModel().create_movie_genre_table()
    MovieCompanyModel().create_movie_company_table()
    MovieHistoryModel().create_movie_history_table()
    LikeModel().create_like_table()
    SavedModel().create_saved_table()
    UserMovieModel().create_user_movie_table()
    return None


def if_not_used():
    create_is_used_table_query()
    insert_is_used_query()

    if not is_used():
        before_run()
        update_is_used_query()
    return None
