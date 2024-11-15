from database_config.db_settings import execute_query


class LanguageModel:
    table_name = "language"
    def create_language_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_language(self, name):
        query = f"""
        INSERT INTO {self.table_name} (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_language(self, language_id, new_name):
        query = f"""
        UPDATE {self.table_name}
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, language_id))
        return None

    def delete_language(self, language_id):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE id = %s;
        """
        execute_query(query, (language_id,))
        return None

    def get_language_by_id(self, language_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE id = %s;
        """
        data = execute_query(query, (language_id,), fetch='one')
        return data

    def get_language_by_name(self, language_name):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE name = %s;
        """
        data = execute_query(query, (language_name,), fetch='one')
        return data

    def get_all_languages(self):
        query = f"""
        SELECT * FROM {self.table_name};
        """
        data = execute_query(query, fetch='all')
        return data