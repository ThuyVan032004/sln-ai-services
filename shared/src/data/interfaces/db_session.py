from abc import ABC, abstractmethod


class IDbSession(ABC):
    @abstractmethod
    def get_session(self):
        pass