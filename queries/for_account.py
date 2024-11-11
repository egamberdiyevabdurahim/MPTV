from database_config.db_settings import execute_query


class AccountModel:
    @staticmethod
    def create_account_table():
        query = """
        CREATE TABLE IF NOT EXISTS account (
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

    @staticmethod
    def create_account(first_name, telegram_id, user_id=None, last_name=None, telegram_username=None):
        query = """
        INSERT INTO account (user_id, first_name, telegram_id, last_name, telegram_username)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
        """
        # Execute the query and return the new user_id if successfully inserted
        user_id = execute_query(query, (user_id, first_name, telegram_id, last_name, telegram_username), fetch='return')
        return user_id  # Returns the user_id if inserted, or None if already exists

    @staticmethod
    def update_account(account_id, user_id=None, first_name=None, last_name=None, telegram_username=None):
        query = """
        UPDATE account
        SET user_id = %s, first_name=%s, last_name=%s, telegram_username=%s, updated_at=NOW()
        WHERE id=%s;
        """
        execute_query(query, (user_id, first_name, last_name, telegram_username, account_id))
        return None

    @staticmethod
    def add_used(account_id):
        used = execute_query("SELECT used FROM account WHERE id=%s;", (account_id,), fetch='one')[0]
        query = """
        UPDATE account
        SET used=%s, updated_at=NOW()
        WHERE id=%s;
        """
        execute_query(query, (int(used)+1, account_id))
        return None

    @staticmethod
    def delete_account(account_id):
        query = """
        UPDATE account
        SET deleted_at=NOW(), status=FALSE
        WHERE id=%s;
        """
        execute_query(query, (account_id,))
        return None

    @staticmethod
    def get_account_by_id(account_id):
        query = """
        SELECT * FROM account
        WHERE id=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (account_id,), fetch='one')

    @staticmethod
    def get_account_by_telegram_id(telegram_id):
        query = """
        SELECT * FROM account
        WHERE telegram_id=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (telegram_id,), fetch='one')

    @staticmethod
    def get_account_by_telegram_username(telegram_username):
        query = """
        SELECT * FROM account
        WHERE telegram_username=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (telegram_username,), fetch='one')

    @staticmethod
    def get_accounts_by_user_id(user_id):
        query = """
        SELECT * FROM account
        WHERE user_id=%s AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, (user_id,), fetch='all')

    @staticmethod
    def get_unauthorized_accounts():
        query = """
        SELECT * FROM account
        WHERE user_id IS NULL AND status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, fetch='all')

    @staticmethod
    def get_all_accounts():
        query = """
        SELECT * FROM account
        WHERE status=TRUE AND deleted_at IS NULL;
        """
        return execute_query(query, fetch='all')

    @staticmethod
    def is_account_registered(telegram_id):
        query = """
        SELECT *
        FROM account
        WHERE telegram_id = %s
        AND status = TRUE
        AND user_id IS NOT NULL
        AND deleted_at IS NULL
        AND is_logout = FALSE
        """
        return True if execute_query(query, (telegram_id,), fetch='one') else False

    @staticmethod
    def logout(telegram_id):
        query = """
        UPDATE account
        SET is_logout = TRUE
        WHERE telegram_id = %s
        AND status = TRUE
        AND user_id IS NOT NULL
        AND deleted_at IS NULL
        """
        execute_query(query, (telegram_id,))
        return None

    @staticmethod
    def update_logout_status(telegram_id):
        query = """
        UPDATE account
        SET is_logout = FALSE
        WHERE telegram_id = %s
        AND status = TRUE
        AND user_id IS NOT NULL
        AND deleted_at IS NULL
        """
        execute_query(query, (telegram_id,))
        return None

    @staticmethod
    def get_all_accounts_by_days(start_date, end_date):
        query = """
        SELECT * FROM account
        WHERE created_at BETWEEN %s AND %s
        AND status = TRUE
        AND deleted_at IS NULL;
        """
        return execute_query(query, (start_date, end_date), fetch='all')