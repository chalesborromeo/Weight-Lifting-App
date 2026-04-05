from abc import ABC, abstractmethod

from app.db.connections import DBConnection
from app.db.repositories import DBRepository

class DBFactory(ABC):
    @classmethod
    @abstractmethod
    def create_db_repository(cls) -> DBRepository:pass

    @classmethod
    @abstractmethod
    def create_db_connection(cls) -> DBConnection:pass

