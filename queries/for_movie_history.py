from database_config.db_settings import execute_query


class MovieHistoryModel:
    def create_movie_history_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS movie_history (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            movie_id BIGINT REFERENCES movie(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );"""
        execute_query(query)
        return None

    def create_movie_history(self, user_id, movie_id):
        query = """
        INSERT INTO movie_history (user_id, movie_id)
        VALUES (%s, %s);
        """
        execute_query(query, (user_id, movie_id))
        return None

    def get_movie_histories_by_user_id(self, user_id):
        query = """
        SELECT * FROM movie_history
        WHERE user_id = %s;
        """
        return execute_query(query, (user_id,), fetch='all')

    def get_all_movie_histories(self):
        query = """
        SELECT * FROM movie_history;
        """
        return execute_query(query, fetch='all')