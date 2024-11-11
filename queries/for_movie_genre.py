from database_config.db_settings import execute_query


class MovieGenreModel:
    def create_movie_genre_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS movie_genre (
            id BIGSERIAL PRIMARY KEY,
            movie_id BIGINT REFERENCES movie(id),
            genre_id BIGINT REFERENCES genre(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )"""
        execute_query(query)
        return None

    def create_movie_genre(self, movie_id, genre_id):
        query = """
        INSERT INTO movie_genre (movie_id, genre_id)
        VALUES (%s, %s);
        """
        execute_query(query, (movie_id, genre_id))
        return None

    def delete_movie_genre(self, movie_id, genre_id):
        query = """
        DELETE FROM movie_genre
        WHERE movie_id = %s AND genre_id = %s;
        """
        execute_query(query, (movie_id, genre_id))
        return None

    def get_all_genres_by_movie_id(self, movie_id):
        query = """
        SELECT *
        FROM movie_genre
        JOIN genre ON movie_genre.genre_id = genre.id
        WHERE movie_genre.movie_id = %s;
        """
        return execute_query(query, (movie_id,), fetch='all')
