from abc import ABC, abstractmethod

class DBRepository(ABC):
    # User
    @abstractmethod
    def get_all_users(self, session): pass

    @abstractmethod
    def save_user(self, user, session): pass

    @abstractmethod
    def get_user(self, user_id, session): pass

    # Club
    @abstractmethod
    def get_all_clubs(self, session): pass

    @abstractmethod
    def get_club(self, club_id, session): pass

    @abstractmethod
    def save_club(self, club, session): pass

    @abstractmethod
    def delete_club(self, club_id, session): pass

    # Workout
    @abstractmethod
    def get_all_workouts(self, session): pass

    @abstractmethod
    def get_users_workouts(self, user_id, session): pass

    @abstractmethod
    def get_workout(self, workout_id, session): pass

    @abstractmethod
    def save_workout(self, workout, session): pass

    @abstractmethod
    def delete_workout(self, workout_id, session): pass


