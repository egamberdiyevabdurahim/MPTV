from database_config.db_settings import execute_query


class UserModel:
    table_name = "users"
    def create_user_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
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

    def create_user(self, username, password, email=None):
        query = f"INSERT INTO {self.table_name} (username, password, email) VALUES (%s, %s, %s) RETURNING id;"
        user_data = execute_query(query, (username, password, email), fetch='return')
        return user_data

    def update_user_password(self, user_id, password):
        query = f"UPDATE {self.table_name} SET password = %s, updated_at = NOW() WHERE id = %s;"
        execute_query(query, (password, user_id))
        return None

    def delete_user(self, user_id):
        query = f"UPDATE {self.table_name} SET status = %s, deleted_at = NOW() WHERE id = %s;"
        execute_query(query, (False, user_id))
        return None

    def get_user_by_id(self, user_id):
        query = f"SELECT * FROM {self.table_name} WHERE id = %s AND status = %s;"
        return execute_query(query, (user_id, True), fetch='one')

    def get_user_by_username(self, username):
        query = f"SELECT * FROM {self.table_name} WHERE username = %s AND status = %s;"
        return execute_query(query, (username, True), fetch='one')

    def get_user_by_username_and_password(self, username, password):
        query = f"SELECT * FROM {self.table_name} WHERE username = %s AND password = %s AND status = %s;"
        return execute_query(query, (username, password, True), fetch='one')

    def get_users_by_email(self, email):
        query = f"SELECT * FROM {self.table_name} WHERE email = %s AND status = %s;"
        return execute_query(query, (email, True), fetch='all')

    def get_all_users(self):
        query = f"SELECT * FROM {self.table_name} WHERE status = %s;"
        return execute_query(query, (True,), fetch='all')