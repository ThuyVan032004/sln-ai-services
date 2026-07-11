from abc import ABC, abstractmethod
from typing import List

class IDomainService(ABC):
    pass

class IDomainService[T](ABC, IDomainService):
    @abstractmethod
    async def get_all(self):
        pass
    
    @abstractmethod
    async def find_by(self, filter):
        pass
    
    @abstractmethod
    async def add(self, entity: T):
        pass
    
    @abstractmethod
    async def update(self, entity: T):
        pass
    
    @abstractmethod
    async def delete(self, entity: T):
        pass
    
    @abstractmethod
    async def add_range(self, entities: List[T]):
        pass
    
    @abstractmethod
    async def update_range(self, entities: List[T]):
        pass
    
    @abstractmethod
    async def delete_range(self, entities: List[T]):
        pass
    
    
    
    
    
    