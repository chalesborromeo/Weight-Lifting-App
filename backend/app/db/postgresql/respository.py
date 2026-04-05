
from app.db.repositories import DBRepository


class PostgreSQLRepository(DBRepository):
    
    def __init__(self, connection):
        self.connection = connection