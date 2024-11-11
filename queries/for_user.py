from database_config.db_settings import execute_query


class UserModel:
    @staticmethod
    def create_user_table():
        query = """
        CREATE TABLE IF NOT EXISTS users (
            id BIGSERIAL PRIMARY KEY,
            username VARCHAR(255),
            password VARCHAR(255),
            email VARCHAR(255),
            is_admin BOOLEAN DEFAULT FALSE,
            is_super BOOLEAN DEFAULT FALSE,
            status BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            deleted_at TIMESTAMPTZ
        );
        """
        execute_query(query)
        return None

    @staticmethod
    def create_user(username, password, email=None):
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s) RETURNING id;"
        user_data = execute_query(query, (username, password, email), fetch='return')
        return user_data

    @staticmethod
    def update_user_password(user_id, password):
        query = "UPDATE users SET password = %s, updated_at = NOW() WHERE id = %s;"
        execute_query(query, (password, user_id))
        return None

    @staticmethod
    def delete_user(user_id):
        query = "UPDATE users SET status = %s, deleted_at = NOW() WHERE id = %s;"
        execute_query(query, (False, user_id))
        return None

    @staticmethod
    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %s AND status = %s;"
        return execute_query(query, (user_id, True), fetch='one')

    @staticmethod
    def get_user_by_username(username):
        query = "SELECT * FROM users WHERE username = %s AND status = %s;"
        return execute_query(query, (username, True), fetch='one')

    @staticmethod
    def get_user_by_username_and_password(username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s AND status = %s;"
        return execute_query(query, (username, password, True), fetch='one')

    @staticmethod
    def get_users_by_email(email):
        query = "SELECT * FROM users WHERE email = %s AND status = %s;"
        return execute_query(query, (email, True), fetch='all')

    @staticmethod
    def get_all_users():
        query = "SELECT * FROM users WHERE status = %s;"
        return execute_query(query, (True,), fetch='all')