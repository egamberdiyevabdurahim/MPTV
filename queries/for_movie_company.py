from database_config.db_settings import execute_query


class MovieCompanyModel:
    def create_movie_company_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS movie_company (
            id BIGSERIAL PRIMARY KEY,
            movie_id BIGINT REFERENCES movie(id),
            company_id BIGINT REFERENCES company(id),
            created_at TIMESTAMPTZ DEFAULT NOW()
        )"""
        execute_query(query)
        return None

    def create_movie_company(self, movie_id, company_id):
        query = """
        INSERT INTO movie_company (movie_id, company_id)
        VALUES (%s, %s);
        """
        execute_query(query, (movie_id, company_id))
        return None

    def delete_movie_company(self, movie_id, company_id):
        query = """
        DELETE FROM movie_company
        WHERE movie_id = %s AND company_id = %s;
        """
        execute_query(query, (movie_id, company_id))
        return None

    def get_all_companies_by_movie_id(self, movie_id):
        query = """
        SELECT *
        FROM movie_company
        JOIN company ON movie_company.company_id = company.id
        WHERE movie_company.movie_id = %s;
        """
        return execute_query(query, (movie_id,), fetch='all')
