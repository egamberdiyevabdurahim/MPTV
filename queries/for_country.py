from database_config.db_settings import execute_query


class CountryModel:
    def create_country_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS country (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_country(self, name):
        query = """
        INSERT INTO country (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_country(self, country_id, new_name):
        query = """
        UPDATE country
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, country_id))
        return None

    def delete_country(self, country_id):
        query = """
        DELETE FROM country
        WHERE id = %s;
        """
        execute_query(query, (country_id,))
        return None

    def get_country_by_id(self, country_id):
        query = """
        SELECT * FROM country
        WHERE id = %s;
        """
        data = execute_query(query, (country_id,), fetch='one')
        return data

    def get_country_by_name(self, country_name):
        query = """
        SELECT * FROM country
        WHERE name = %s;
        """
        data = execute_query(query, (country_name,), fetch='one')
        return data

    def get_all_countries(self):
        query = """
        SELECT * FROM country;
        """
        data = execute_query(query, fetch='all')
        return data