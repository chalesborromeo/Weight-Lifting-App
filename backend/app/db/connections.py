from abc import ABC, abstractmethod

class DBConnection(ABC):
    @abstractmethod
    def get_session(self): pass

    @abstractmethod
    def disconnect(self): pass

    @classmethod
    @abstractmethod
    def get_instance(cls): pass