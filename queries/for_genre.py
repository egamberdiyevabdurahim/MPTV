from database_config.db_settings import execute_query


class GenreModel:
    def create_genre_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS genre (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_genre(self, name):
        query = """
        INSERT INTO genre (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_genre(self, genre_id, new_name):
        query = """
        UPDATE genre
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, genre_id))
        return None

    def delete_genre(self, genre_id):
        query = """
        DELETE FROM genre
        WHERE id = %s;
        """
        execute_query(query, (genre_id,))
        return None

    def get_genre_by_id(self, genre_id):
        query = """
        SELECT * FROM genre
        WHERE id = %s;
        """
        data = execute_query(query, (genre_id,), fetch='one')
        return data

    def get_genre_by_name(self, genre_name):
        query = """
        SELECT * FROM genre
        WHERE name = %s;
        """
        data = execute_query(query, (genre_name,), fetch='one')
        return data

    def get_all_genres(self):
        query = """
        SELECT * FROM genre;
        """
        data = execute_query(query, fetch='all')
        return data