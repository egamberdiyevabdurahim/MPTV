from database_config.db_settings import execute_query


class LanguageModel:
    def create_language_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS language (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_language(self, name):
        query = """
        INSERT INTO language (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_language(self, language_id, new_name):
        query = """
        UPDATE language
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, language_id))
        return None

    def delete_language(self, language_id):
        query = """
        DELETE FROM language
        WHERE id = %s;
        """
        execute_query(query, (language_id,))
        return None

    def get_language_by_id(self, language_id):
        query = """
        SELECT * FROM language
        WHERE id = %s;
        """
        data = execute_query(query, (language_id,), fetch='one')
        return data

    def get_language_by_name(self, language_name):
        query = """
        SELECT * FROM language
        WHERE name = %s;
        """
        data = execute_query(query, (language_name,), fetch='one')
        return data

    def get_all_languages(self):
        query = """
        SELECT * FROM language;
        """
        data = execute_query(query, fetch='all')
        return data