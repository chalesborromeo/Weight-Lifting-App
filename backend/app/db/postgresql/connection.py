from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.connections import DBConnection
from app.core.config import settings

class PostgreSQLConnection(DBConnection):
    _instance = None

    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)

    @contextmanager
    def get_session(self):
        session = self.SessionLocal() # create a new session

        try:
            yield session # hand session to 'with' statement
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def disconnect(self):
        self.engine.dispose()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = PostgreSQLConnection()

        return cls._instance
