from database_config.db_settings import execute_query
from queries.for_company import CompanyModel


class MovieCompanyModel:
    table_name = "movie_company"
    def create_movie_company_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            movie_id BIGINT REFERENCES movie(id),
            company_id BIGINT REFERENCES company(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )"""
        execute_query(query)
        return None

    def create_movie_company(self, movie_id, company_id):
        query = f"""
        INSERT INTO {self.table_name} (movie_id, company_id)
        VALUES (%s, %s);
        """
        execute_query(query, (movie_id, company_id))
        return None

    def delete_movie_company(self, movie_id, company_id):
        query = f"""
        DELETE FROM {self.table_name}
        WHERE movie_id = %s AND company_id = %s;
        """
        execute_query(query, (movie_id, company_id))
        return None

    def get_all_companies_by_movie_id(self, movie_id):
        query = f"""
        SELECT *
        FROM {self.table_name}
        JOIN {CompanyModel().table_name} ON movie_company.company_id = company.id
        WHERE movie_company.movie_id = %s;
        """
        return execute_query(query, (movie_id,), fetch='all')
