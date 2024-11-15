from database_config.db_settings import execute_query


class CountryModel:
    table_name = "country"
    def create_country_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_country(self, name):
        query = f"""
        INSERT INTO {self.table_name} (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_country(self, country_id, new_name):
        query = f"""
        UPDATE {self.table_name}
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, country_id))
        return None

    def delete_country(self, country_id):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE id = %s;
        """
        execute_query(query, (country_id,))
        return None

    def get_country_by_id(self, country_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE id = %s;
        """
        data = execute_query(query, (country_id,), fetch='one')
        return data

    def get_country_by_name(self, country_name):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE name = %s;
        """
        data = execute_query(query, (country_name,), fetch='one')
        return data

    def get_all_countries(self):
        query = f"""
        SELECT * FROM {self.table_name};
        """
        data = execute_query(query, fetch='all')
        return data