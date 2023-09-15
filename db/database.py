import sqlite3

from loguru import logger
from db import sql_queries


class DataBase:
    """
    Manages database
    """
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def startup(self):
        """
        DB startup that creates metro_news table
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql_queries.CREATE_NEWS_TABLE)
            logger.debug("Created table metro_news")
        except sqlite3.Error as e:
            logger.debug(f"Error starting up database: {e}")

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logger.debug(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")

    def execute_query(self, query: str, params: list = None) -> None:
        try:
            if params:
                self.cursor.execute(query, (*params,))
            else:
                self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error executing query: {e}")

    def fetch_data(self, query: str, params: list = None) -> tuple[str] | None:
        try:
            if params:
                self.cursor.execute(query, (*params,))
            else:
                self.cursor.execute(query)
            data = self.cursor.fetchall()
            return data
        except sqlite3.Error as e:
            logger.error(f"Error fetching data: {e}")
            return None

    def commit_transaction(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error committing transaction: {e}")

    def close(self):
        if self.conn:
            self.conn.close()
            logger.debug("Closed database connection")
