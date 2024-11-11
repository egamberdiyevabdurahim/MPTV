from database_config.db_settings import execute_query


class MovieModel:
    def create_movie_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS movie (
            id BIGSERIAL PRIMARY KEY,
            movie_id_360 TEXT,
            movie_id_480 TEXT,
            movie_id_720 TEXT,
            movie_id_1080 TEXT,
            code BIGINT,
            title VARCHAR(255),
            release_date INT,
            duration INT,
            category_id INT REFERENCES category(id),
            language_id INT REFERENCES language(id),
            country_id INT REFERENCES country(id),
            views BIGINT DEFAULT 0,
            status BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            deleted_at TIMESTAMPTZ
        )"""
        execute_query(query)
        return None

    def create_movie(self, title, release_date, duration, language_id, country_id,
                     movie_id_360, movie_id_480, movie_id_720, movie_id_1080, code, category_id):
        query = """
        INSERT INTO movie (title, release_date, duration, language_id, country_id,
                          movie_id_360, movie_id_480, movie_id_720, movie_id_1080, code, category_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        result = execute_query(query, (title, release_date, duration,
                                       language_id, country_id, movie_id_360, movie_id_480,
                                       movie_id_720, movie_id_1080, code, category_id
                                       ), fetch='return')
        return result

    def update_movie(self, movie_id, title=None, release_date=None, duration=None,
                     language_id=None, country_id=None, movie_id_360=None,
                     movie_id_480=None, movie_id_720=None, movie_id_1080=None, category_id=None):
        query = """
        UPDATE movie SET title = %s, release_date = %s, duration = %s,
        language_id = %, country_id = %s, movie_id_360 = %s,
        movie_id_480 = %s, movie_id_720 = %s, movie_id_1080 = %s, category_id = %s
        WHERE id = %s"""
        execute_query(query, (title, release_date, duration,
                              language_id, country_id, movie_id_360, movie_id_480,
                              movie_id_720, movie_id_1080, category_id, movie_id))
        return None

    def delete_movie(self, movie_id):
        query = "UPDATE movie SET status=%s AND deleted_at=NOW() WHERE id=%s"
        execute_query(query, (False, movie_id))
        return None

    def add_view_count(self, movie_id):
        query = "UPDATE movie SET views=views+1 WHERE id=%s"
        execute_query(query, (movie_id,))
        return None

    def get_movie_by_id(self, movie_id):
        query = "SELECT * FROM movie WHERE id=%s AND status=TRUE"
        return execute_query(query, (movie_id,), fetch='one')

    def get_movie_by_code(self, code):
        query = "SELECT * FROM movie WHERE code=%s AND status=TRUE"
        return execute_query(query, (code,), fetch='one')

    def get_movies_by_category_id(self, category_id):
        query = "SELECT * FROM movie WHERE category_id=%s AND status=TRUE"
        return execute_query(query, (category_id,), fetch='all')

    def get_movies_by_language_id(self, language_id):
        query = "SELECT * FROM movie WHERE language_id=%s AND status=TRUE"
        return execute_query(query, (language_id,), fetch='all')

    def get_movies_by_country_id(self, country_id):
        query = "SELECT * FROM movie WHERE country_id=%s AND status=TRUE"
        return execute_query(query, (country_id,), fetch='all')

    def get_movies_by_release_date(self, release_date):
        query = "SELECT * FROM movie WHERE release_date=%s AND status=TRUE"
        return execute_query(query, (release_date,), fetch='all')

    def get_movies_by_duration(self, duration):
        query = "SELECT * FROM movie WHERE duration=%s AND status=TRUE"
        return execute_query(query, (duration,), fetch='all')

    def get_most_viewed_movies(self, limit):
        query = f"""
        SELECT *
        FROM movie
        WHERE status=TRUE AND views > 0
        ORDER BY views DESC
        LIMIT {limit};
        """
        return execute_query(query, fetch='all')

    def get_most_recent_movies(self, limit):
        query = f"""
        SELECT *
        FROM movie
        WHERE status=TRUE
        ORDER BY release_date DESC
        LIMIT {limit};
        """
        return execute_query(query, fetch='all')

    def get_most_recent_added_movies(self, limit):
        query = f"""
        SELECT *
        FROM movie
        WHERE status=TRUE
        ORDER BY created_at DESC
        LIMIT {limit};
        """
        return execute_query(query, fetch='all')

    def get_top_liked_movies(self, limit):
        query = """
        SELECT m.*, COUNT(*) AS counter
        FROM like_movie lm
        JOIN movie m ON lm.movie_id = m.id
        WHERE m.status = TRUE
        GROUP BY m.id
        ORDER BY counter DESC
        LIMIT %s;
        """
        return execute_query(query, params=(limit,), fetch='all')

    def get_movies_by_genre_id(self, genre_id):
        query = f"""
        SELECT m.*
        FROM movie_genre mg
        JOIN movie m ON m.id = mg.movie_id
        WHERE mg.genre_id = %s AND m.status=TRUE
        GROUP BY m.id, m.title;
        """
        return execute_query(query, (genre_id,), fetch='all')

    def get_movies_by_company_id(self, company_id):
        query = f"""
        SELECT m.*
        FROM movie_company mc
        JOIN movie m ON m.id = mc.movie_id
        WHERE mc.company_id = %s AND m.status=TRUE
        GROUP BY m.id, m.title;
        """
        return execute_query(query, (company_id,), fetch='all')

    def get_movies_by_year(self, year):
        query = f"""
        SELECT *
        FROM movie
        WHERE release_date = %s AND status=TRUE
        ORDER BY release_date DESC;
        """
        return execute_query(query, (year,), fetch='all')

    def get_all_movies(self):
        query = "SELECT * FROM movie WHERE status=TRUE"
        return execute_query(query, fetch='all')

    def get_movies_by_search(self, search_query):
        query = f"""
        SELECT *
        FROM movie
        WHERE LOWER(title) ILIKE LOWER('%{search_query}%') AND status=TRUE
        ORDER BY release_date DESC;
        """
        return execute_query(query, fetch='all')

    def get_last_movie(self):
        query = "SELECT * FROM movie WHERE status=TRUE ORDER BY id DESC LIMIT 1"
        return execute_query(query, fetch='one')

    def get_likes_count(self, movie_id):
        query = """
        SELECT COUNT(*) FROM like_movie WHERE movie_id = %s;
        """
        likes_count = execute_query(query, (movie_id,), fetch='one')
        return likes_count[0]

    def get_movies_year(self):
        query = """
        SELECT release_date, COUNT(*) as counter
        FROM movie
        GROUP BY release_date
        ORDER BY release_date DESC;
        """
        return execute_query(query, fetch='all')