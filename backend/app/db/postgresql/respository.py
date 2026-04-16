
from app.db.repositories import DBRepository
from app.models.user import User


class PostgreSQLRepository(DBRepository):

    def get_all_users(self, session):
        return session.query(User).all()


    def save_user(self, user, session):
        session.add(user)
        session.flush()
        return user


    def get_user(self, user_id, session):
        return session.query(User).filter(User.id == user_id).first()
