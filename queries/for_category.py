from database_config.db_settings import execute_query


class CategoryModel:
    table_name = "category"
    def create_category_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_category(self, name):
        query = f"""
        INSERT INTO {self.table_name} (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_category(self, category_id, new_name):
        query = f"""
        UPDATE {self.table_name}
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, category_id))
        return None

    def delete_category(self, category_id):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE id = %s;
        """
        execute_query(query, (category_id,))
        return None

    def get_category_by_id(self, category_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE id = %s;
        """
        data = execute_query(query, (category_id,), fetch='one')
        return data

    def get_category_by_name(self, category_name):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE name = %s;
        """
        data = execute_query(query, (category_name,), fetch='one')
        return data

    def get_all_categories(self):
        query = f"""
        SELECT * FROM {self.table_name};
        """
        data = execute_query(query, fetch='all')
        return data