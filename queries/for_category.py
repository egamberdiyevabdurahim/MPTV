from database_config.db_settings import execute_query


class CategoryModel:
    def create_category_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS category (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_category(self, name):
        query = """
        INSERT INTO category (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_category(self, category_id, new_name):
        query = """
        UPDATE category
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, category_id))
        return None

    def delete_category(self, category_id):
        query = """
        DELETE FROM category
        WHERE id = %s;
        """
        execute_query(query, (category_id,))
        return None

    def get_category_by_id(self, category_id):
        query = """
        SELECT * FROM category
        WHERE id = %s;
        """
        data = execute_query(query, (category_id,), fetch='one')
        return data

    def get_category_by_name(self, category_name):
        query = """
        SELECT * FROM category
        WHERE name = %s;
        """
        data = execute_query(query, (category_name,), fetch='one')
        return data

    def get_all_categories(self):
        query = """
        SELECT * FROM category;
        """
        data = execute_query(query, fetch='all')
        return data