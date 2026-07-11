from abc import ABC, abstractmethod

    
class IUnitOfWork(ABC):
    @abstractmethod
    async def commit(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass
    