from abc import ABC, abstractmethod


class IDbSession(ABC):
    @abstractmethod
    async def get_session(self):
        pass