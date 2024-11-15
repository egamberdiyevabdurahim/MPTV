from database_config.db_settings import execute_query
from queries.for_genre import GenreModel


class MovieGenreModel:
    table_name = "movie_genre"
    def create_movie_genre_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            movie_id BIGINT REFERENCES movie(id),
            genre_id BIGINT REFERENCES genre(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )"""
        execute_query(query)
        return None

    def create_movie_genre(self, movie_id, genre_id):
        query = f"""
        INSERT INTO {self.table_name} (movie_id, genre_id)
        VALUES (%s, %s);
        """
        execute_query(query, (movie_id, genre_id))
        return None

    def delete_movie_genre(self, movie_id, genre_id):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE movie_id = %s AND genre_id = %s;
        """
        execute_query(query, (movie_id, genre_id))
        return None

    def get_all_genres_by_movie_id(self, movie_id):
        query = f"""
        SELECT *
        FROM {self.table_name}
        JOIN {GenreModel().table_name} ON movie_genre.genre_id = genre.id
        WHERE movie_genre.movie_id = %s;
        """
        return execute_query(query, (movie_id,), fetch='all')
