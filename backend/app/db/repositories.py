from abc import ABC, abstractmethod

class DBRepository(ABC):
    @abstractmethod
    def get_all_users(self): pass

    @abstractmethod
    def save_user(self, user): pass

    @abstractmethod
    def get_user(self, user_id): pass
