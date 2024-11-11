from database_config.db_settings import execute_query


class LikeModel:
    def create_like_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS like_movie (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            movie_id BIGINT REFERENCES movie(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        );"""
        execute_query(query)
        return None

    def create_like(self, user_id, movie_id):
        query = """
        INSERT INTO like_movie (user_id, movie_id)
        VALUES (%s, %s) RETURNING id;
        """
        like_id = execute_query(query, (user_id, movie_id), fetch='return')
        return like_id

    def delete_like(self, user_id, movie_id):
        query = "DELETE FROM like_movie WHERE user_id=%s AND movie_id=%s"
        execute_query(query, (user_id, movie_id))
        return None

    def get_likes_by_movie_id(self, movie_id):
        query = """
        SELECT * FROM like_movie WHERE movie_id = %s;
        """
        likes = execute_query(query, (movie_id,))
        return likes

    def get_likes_by_user_id(self, user_id):
        query = """
        SELECT * FROM like_movie WHERE user_id = %s;
        """
        likes = execute_query(query, (user_id,), fetch='all')
        return likes

    def get_all_likes(self):
        query = """
        SELECT * FROM like_movie;
        """
        likes = execute_query(query)
        return likes

    def get_like_by_user_id_and_movie_id(self, user_id, movie_id):
        query = """
        SELECT * FROM like_movie WHERE user_id = %s AND movie_id = %s;
        """
        return execute_query(query, (user_id, movie_id), fetch='one')