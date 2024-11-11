from database_config.db_settings import execute_query


class HiddenHistoryModel:
    def create_hidden_history_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS hidden_history (
            id BIGSERIAL PRIMARY KEY,
            account_id BIGINT REFERENCES account(id),
            message_id TEXT,
            text TEXT,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );"""
        execute_query(query)
        return None

    def create_hidden_history(self, account_id, message_id, text=None):
        query = """
        INSERT INTO hidden_history (account_id, message_id, text)
        VALUES (%s, %s, %s);
        """
        execute_query(query, (account_id, message_id, text))
        return None

    def get_hidden_histories_by_account_id(self, account_id):
        query = """
        SELECT * FROM hidden_history
        WHERE account_id = %s;
        """
        return execute_query(query, (account_id,), fetch='all')

    def get_all_hidden_histories(self):
        query = """
        SELECT * FROM hidden_history;
        """
        return execute_query(query, fetch='all')
