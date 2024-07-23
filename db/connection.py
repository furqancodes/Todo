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

    @staticmethod
    def get_connection():
        return Database.connection_pool.getconn()

    @staticmethod
    def return_connection(connection):
        Database.connection_pool.putconn(connection)

    @staticmethod
    def close_all_connections():
        Database.connection_pool.closeall()
