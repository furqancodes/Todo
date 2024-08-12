from sqlalchemy import create_engine
from config.config import Config

class Database:
    engine = None

    @staticmethod
    def initialize():
        if Database.engine is None:
            Database.engine = create_engine(Config['db_url'])

    @staticmethod
    def get_connection():
        if Database.engine is None:
            Database.initialize()
        return Database.engine.connect()

    def __enter__(self):
        self.connection = Database.get_connection()
        self.transaction = self.connection.begin()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.transaction.rollback()
        else:
            self.transaction.commit()
        self.connection.close()
