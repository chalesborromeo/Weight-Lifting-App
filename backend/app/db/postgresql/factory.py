
from app.db.connections import DBConnection
from app.db.factory import DBFactory
from app.db.postgresql.connection import PostgreSQLConnection
from app.db.postgresql.respository import PostgreSQLRepository
from app.db.repositories import DBRepository


class PostgreSQLFactory(DBFactory):
    @classmethod
    def create_db_connection(cls) -> DBConnection:
        return PostgreSQLConnection.get_instance()

    @classmethod
    def create_db_repository(cls) -> DBRepository:
        return PostgreSQLRepository()