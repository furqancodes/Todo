from psycopg2 import pool
from config.config import Config

class Database:
    connection_pool = None

    @staticmethod
    def initialize():
        Database.connection_pool = pool.SimpleConnectionPool(
            1,
            10,
            database=Config.get('dbname'),
            user=Config.get('user'),
            password=Config.get('password'),
            host=Config.get('host'),
            port=Config.get("port")
        )

    def __enter__(self):
        self.connection = Database.get_connection()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        Database.return_connection(self.connection)

    @staticmethod
    def get_connection():
        return Database.connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.connection_pool.closeall()
