from database_config.db_settings import execute_query


class SavedModel:
    table_name = "saved"
    def create_saved_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            movie_id BIGINT REFERENCES movie(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );"""
        execute_query(query)
        return None

    def create_saved(self, user_id, movie_id):
        query = f"""
        INSERT INTO {self.table_name} (user_id, movie_id)
        VALUES (%s, %s)
        RETURNING id;
        """
        result = execute_query(query, (user_id, movie_id), fetch='return')
        return result

    def delete_saved(self, user_id, movie_id):
        query = f"DELETE FROM {self.table_name} WHERE user_id=%s AND movie_id=%s"
        execute_query(query, (user_id, movie_id))
        return None

    def get_saved_movies_by_user_id(self, user_id):
        query = f"SELECT * FROM {self.table_name} WHERE user_id=%s"
        return execute_query(query, (user_id,), fetch='all')

    def get_all_saved(self):
        query = f"SELECT * FROM {self.table_name}"
        return execute_query(query, fetch='all')

    def get_saved_by_user_id_and_movie_id(self, user_id, movie_id):
        query = f"SELECT * FROM {self.table_name} WHERE user_id=%s AND movie_id=%s"
        return execute_query(query, (user_id, movie_id), fetch='one')