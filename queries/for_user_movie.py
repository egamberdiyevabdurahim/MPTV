from database_config.db_settings import execute_query


class UserMovieModel:
    def create_user_movie_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS user_movie (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            movie_id BIGINT REFERENCES movie(id),
            watched BOOLEAN DEFAULT TRUE,
            last_watched_time TIMESTAMPTZ,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        execute_query(query)
        return None

    def create_movie(self, user_id, movie_id):
        query = "INSERT INTO user_movie (user_id, movie_id) VALUES (%s, %s);"
        execute_query(query, (user_id, movie_id))
        return None

    def mark_as_watched(self, user_id, movie_id):
        query = "UPDATE user_movie SET watched = TRUE, last_watched_time = NOW() WHERE user_id = %s AND movie_id = %s;"
        execute_query(query, (user_id, movie_id))
        return None

    def unmark_as_watched(self, user_id, movie_id):
        query = "UPDATE user_movie SET watched = FALSE WHERE user_id = %s AND movie_id = %s;"
        execute_query(query, (user_id, movie_id))

    def get_watched_movies(self, user_id):
        query = "SELECT * FROM user_movie WHERE user_id = %s AND watched = TRUE;"
        return execute_query(query, (user_id,), fetch='all')

    def get_unwatched_movies(self, user_id):
        query = "SELECT * FROM user_movie WHERE user_id = %s AND watched = FALSE;"
        return execute_query(query, (user_id,), fetch='all')

    def get_all_user_movie(self):
        query = "SELECT * FROM user_movie;"
        return execute_query(query, fetch='all')

    def get_by_user_id_and_movie_id(self, user_id, movie_id):
        query = "SELECT * FROM user_movie WHERE user_id = %s AND movie_id = %s;"
        return execute_query(query, (user_id, movie_id), fetch='one')