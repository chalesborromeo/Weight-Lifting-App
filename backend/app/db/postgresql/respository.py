
from app.db.repositories import DBRepository
from app.models.user import User
from app.models.club import Club
from app.models.workout import Workout


class PostgreSQLRepository(DBRepository):

    def get_user_by_email(self, email, session):
        return session.query(User).filter(User.email == email).first()

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
    
    # Workout
    def get_all_workouts(self, session):
        return session.query(Workout).all()
    
    def get_users_workouts(self, user_id, session):
        return session.query(Workout).filter(Workout.user_id == user_id).all()
    
    def get_workout(self, workout_id, session):
        return session.query(Workout).filter(Workout.id == workout_id).first()

    def save_workout(self, workout, session):
        session.add(workout)
        session.flush()
        return workout
    
    def delete_workout(self, workout_id, session):
        workout = session.query(Workout).filter(Workout.id == workout_id).first()
        if workout:
            session.delete(workout)
            session.flush()

        return workout
    