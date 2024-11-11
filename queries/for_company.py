from database_config.db_settings import execute_query


class CompanyModel:
    def create_company_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS company (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_company(self, name):
        query = """
        INSERT INTO company (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_company(self, company_id, new_name):
        query = """
        UPDATE company
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, company_id))
        return None

    def delete_company(self, company_id):
        query = """
        DELETE FROM company
        WHERE id = %s;
        """
        execute_query(query, (company_id,))
        return None

    def get_company_by_id(self, company_id):
        query = """
        SELECT * FROM company
        WHERE id = %s;
        """
        data = execute_query(query, (company_id,), fetch='one')
        return data

    def get_company_by_name(self, company_name):
        query = """
        SELECT * FROM company
        WHERE name = %s;
        """
        data = execute_query(query, (company_name,), fetch='one')
        return data

    def get_all_companies(self):
        query = """
        SELECT * FROM company;
        """
        data = execute_query(query, fetch='all')
        return data