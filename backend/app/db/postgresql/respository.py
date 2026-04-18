
from app.db.repositories import DBRepository
from app.models.user import User
from app.models.club import Club


class PostgreSQLRepository(DBRepository):

    # User
    def get_all_users(self, session):
        return session.query(User).all()

    def save_user(self, user, session):
        session.add(user)
        session.flush()
        return user

    def get_user(self, user_id, session):
        return session.query(User).filter(User.id == user_id).first()

    # Club
    def get_all_clubs(self, session):
        return session.query(Club).all()
    
    def get_club(self, club_id, session):
        return session.query(Club).filter(Club.id == club_id).first()

    def save_club(self, club, session):
        session.add(club)
        session.flush()
        return club
    
    def delete_club(self, club_id, session):
        club = session.query(Club).filter(Club.id == club_id).first()
        if club:
            session.delete(club)
            session.flush()
    
