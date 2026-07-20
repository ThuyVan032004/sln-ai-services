from typing import List

from shared.business.interfaces.domain_service import IDomainService
from shared.data.interfaces.repository import IRepository


class DomainServiceBase[T](IDomainService[T]):
    def __init__(self, repository: IRepository[T]):
        self.repository = repository
    
    async def get_all(self):
        return await self.repository.get_all()
    
    async def find_by(self, filter):
        return await self.repository.find_by(filter)
    
    async def add(self, entity: T):
        return await self.repository.add(entity)
    
    async def update(self, entity: T):
        return await self.repository.update(entity)
    
    async def delete(self, entity: T):
        return await self.repository.delete(entity)

    async def add_range(self, entities: List[T]):
        return await self.repository.add_range(entities)
    
    async def update_range(self, entities: List[T]):
        return await self.repository.update_range(entities)

    async def delete_range(self, entities: List[T]):
        return await self.repository.delete_range(entities)
