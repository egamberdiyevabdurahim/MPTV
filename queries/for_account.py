from database_config.db_settings import execute_query


class AccountModel:
    table_name = 'account'

    def create_account_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(id),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            telegram_username VARCHAR(255),
            used BIGINT DEFAULT 1,
            telegram_id BIGINT,
            is_logout BOOLEAN DEFAULT FALSE, 
            status BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW(),
            deleted_at TIMESTAMPTZ
        );
        """
        execute_query(query)
        return None

    def create_account(self, first_name, telegram_id, user_id=None, last_name=None, telegram_username=None):
        query = f"""
        INSERT INTO {self.table_name} (user_id, first_name, telegram_id, last_name, telegram_username)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        # Execute the query and return the new user_id if successfully inserted
        user_id = execute_query(query, (user_id, first_name, telegram_id, last_name, telegram_username), fetch='return')
        return user_id  # Returns the user_id if inserted, or None if already exists

    def update_account(self, account_id, user_id=None, first_name=None, last_name=None, telegram_username=None):
        query = f"""
        UPDATE {self.table_name}
        SET user_id = %s, first_name=%s, last_name=%s, telegram_username=%s, updated_at=NOW()
        WHERE id=%s;
        """
        execute_query(query, (user_id, first_name, last_name, telegram_username, account_id))
        return None

    def add_used(self, account_id):
        used = execute_query(f"SELECT used FROM {self.table_name} WHERE id=%s;", (account_id,), fetch='one')[0]
        query = f"""
        UPDATE {self.table_name}
        SET used=%s, updated_at=NOW()
        WHERE id=%s;
        """
        execute_query(query, (int(used)+1, account_id))
        return None

    def delete_account(self, account_id):
        query = f"""
        UPDATE {self.table_name}
        SET deleted_at=NOW(), status=FALSE
        WHERE id=%s;
        """
        execute_query(query, (account_id,))
        return None

    def get_account_by_id(self, account_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE id=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (account_id,), fetch='one')

    def get_account_by_telegram_id(self, telegram_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE telegram_id=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (telegram_id,), fetch='one')

    def get_account_by_telegram_username(self, telegram_username):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE telegram_username=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (telegram_username,), fetch='one')

    def get_accounts_by_user_id(self, user_id):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE user_id=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (user_id,), fetch='all')

    def get_unauthorized_accounts(self):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE user_id IS NULL AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, fetch='all')

    def get_all_accounts(self):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, fetch='all')

    def is_account_registered(self, telegram_id):
        query = f"""
        SELECT *
        FROM {self.table_name}
        WHERE telegram_id = %s
        AND status = TRUE
        AND user_id IS NOT NULL
        AND deleted_at IS NULL
        AND is_logout = FALSE
        """
        return True if execute_query(query, (telegram_id,), fetch='one') else False

    def logout(self, telegram_id):
        query = f"""
        UPDATE {self.table_name}
        SET is_logout = TRUE
        WHERE telegram_id = %s
        AND status = TRUE
        AND user_id IS NOT NULL
        AND deleted_at IS NULL
        """
        execute_query(query, (telegram_id,))
        return None

    def update_logout_status(self, telegram_id):
        query = f"""
        UPDATE {self.table_name}
        SET is_logout = FALSE
        WHERE telegram_id = %s
        AND status = TRUE
        AND user_id IS NOT NULL
        AND deleted_at IS NULL
        """
        execute_query(query, (telegram_id,))
        return None

    def get_all_accounts_by_days(self, start_date, end_date):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE created_at BETWEEN %s AND %s
        AND status = TRUE
        AND deleted_at IS NULL;
        """
        return execute_query(query, (start_date, end_date), fetch='all')

    def get_active_accounts_by_days(self, start_date, end_date):
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE updated_at BETWEEN %s AND %s
        AND is_logout = FALSE
        AND status = TRUE
        AND deleted_at IS NULL;
        """
        return execute_query(query, (start_date, end_date), fetch='all')
