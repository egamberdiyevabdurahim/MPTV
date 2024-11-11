import psycopg2
from psycopg2.extras import DictCursor
import logging
from database_config.config import DB_CONFIG


class DatabaseError(Exception):
    """Custom exception for handling database errors."""
    pass


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        except psycopg2.OperationalError as e:
            logging.error(f"Error connecting to the database: {e}")
            raise DatabaseError("Failed to connect to the database.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if self.cursor is not None:
                self.cursor.close()

            if exc_type is not None:
                self.conn.rollback()
                logging.error(f"Error in DB operation: {exc_val}")
            else:
                self.conn.commit()

        finally:
            if self.conn is not None:
                self.conn.close()

    def execute(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE)"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            logging.error(f"Exception during query execution: {e}")
            raise DatabaseError(f"Failed to execute query: {query}")

    def execute_and_fetch(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE) and fetch the result"""
        try:
            self.cursor.execute(query, params)
            data = self.cursor.fetchone()
            self.conn.commit()
            return data
        except Exception as e:
            logging.error(f"Exception during execute_and_fetch: {e}")
            raise DatabaseError(f"Failed to execute query: {query}")

    def fetchall(self, query, params=None):
        """Fetch multiple rows from the database"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            logging.error(f"Exception during fetchall: {e}")
            raise DatabaseError("Failed to fetch data.")

    def fetchone(self, query, params=None):
        """Fetch a single row from the database"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            logging.error(f"Exception during fetchone: {e}")
            raise DatabaseError("Failed to fetch data.")


def execute_query(query, params=None, fetch=None):
    """Run blocking query using asyncio.run_in_executor to prevent blocking the event loop"""
    with Database() as db:
        if fetch == "all":
            return db.fetchall(query, params)
        elif fetch == "one":
            return db.fetchone(query, params)
        elif fetch == "return":
            return db.execute_and_fetch(query, params)
        else:
            db.execute(query, params)
