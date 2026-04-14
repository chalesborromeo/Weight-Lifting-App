from app.db.postgresql.connection import PostgreSQLConnection
from sqlalchemy import text

from app.db.postgresql.factory import PostgreSQLFactory
from app.db.base import Base

def test_connection():
    print("Testing connection:")
    connection = PostgreSQLConnection.get_instance()
    print("Connection instance created")

    with connection.get_session() as session:
        result = session.execute(text("SELECT 1"))
        print(f"Query exectued: {result.fetchone()}")

def test_factory():
    print("Testing Factories:")
    connection = PostgreSQLFactory.create_db_connection()
    print(f"create_db_connection: {connection}")

    repo = PostgreSQLFactory.create_db_repository()
    print(f"create_db_repository: {repo}")

def test_tables():
    print("Testing tables")
    connection = PostgreSQLConnection.get_instance()
    Base.metadata.create_all(bind=connection.engine)
    print("create tables succesfully")

if __name__ == "__main__":
    test_connection()
    test_factory()
    test_tables()