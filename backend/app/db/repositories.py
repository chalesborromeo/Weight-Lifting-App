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



