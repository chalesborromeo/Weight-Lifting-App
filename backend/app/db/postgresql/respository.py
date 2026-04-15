
from app.db.repositories import DBRepository
from app.models.user import User


class PostgreSQLRepository(DBRepository):
    
    def __init__(self, connection):
        self.connection = connection

    def get_all_users(self):
        with self.connection.get_session() as session:
            return session.query(User).all()


    def save_user(self, user):
        with self.connection.get_session() as session:
            session.add(user)
            return user


    def get_user(self, user_id):
        with self.connection.get_session() as session:
            return session.query(User).filter(User.id == user_id).first()
