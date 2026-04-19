from app.db.base import Base
from app.db.postgresql.factory import PostgreSQLFactory
from sqlalchemy import text

connection = PostgreSQLFactory.create_db_connection()

with connection.engine.connect() as conn:
    conn.execute(text("DROP SCHEMA public CASCADE"))
    conn.execute(text("CREATE SCHEMA public"))
    conn.commit()

print("done")