from database_config.db_settings import execute_query


class CompanyModel:
    table_name = "company"
    def create_company_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            name VARCHAR(255)
        )"""
        execute_query(query)
        return None

    def create_company(self, name):
        query = f"""
        INSERT INTO {self.table_name} (name)
        VALUES (%s)
        RETURNING id;
        """
        data = execute_query(query, (name,), fetch='return')
        return data

    def update_company(self, company_id, new_name):
        query = f"""
        UPDATE {self.table_name}
        SET name = %s
        WHERE id = %s;
        """
        execute_query(query, (new_name, company_id))
        return None

    def delete_company(self, company_id):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE id = %s;
        """
        execute_query(query, (company_id,))
        return None

    def get_company_by_id(self, company_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE id = %s;
        """
        data = execute_query(query, (company_id,), fetch='one')
        return data

    def get_company_by_name(self, company_name):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE name = %s;
        """
        data = execute_query(query, (company_name,), fetch='one')
        return data

    def get_all_companies(self):
        query = f"""
        SELECT * FROM {self.table_name};
        """
        data = execute_query(query, fetch='all')
        return data