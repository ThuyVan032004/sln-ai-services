from datetime import datetime
from typing import List, Type, get_args

from sqlalchemy import select

from dependency_injector.providers import Provider

from shared.src.data.interfaces.db_session import IDbSession
from shared.src.data.interfaces.repository import IRepository
from shared.src.data.interfaces.unit_of_work import IUnitOfWork

class RepositoryBase[T](IRepository[T]):
    def __init__(self, db_session: Provider[IDbSession], unit_of_work: Provider[IUnitOfWork]):
        self.db_session = db_session()
        self.unit_of_work = unit_of_work()

    def _resolve_entity_type(self) -> Type[T]:
        return get_args(self.__orig_bases__[0])[0]
    
    def _set_create_audit_fields(self, entity: T):
        entity.created_at = datetime.now()
    
    def _set_update_audit_fields(self, entity: T):
        entity.updated_at = datetime.now()
    
    def _set_delete_audit_fields(self, entity: T):
        entity.deleted_at = datetime.now()
        entity.is_deleted = True
    
    async def get_all(self):
        entity_type = self._resolve_entity_type()
        return await self.db_session.execute(select(entity_type))
    
    async def find_by(self, filter):
        entity_type = self._resolve_entity_type()
        return await self.db_session.execute(select(entity_type).where(filter))
    
    async def add(self, entity: T):
        self._set_create_audit_fields(entity)
        self.db_session.add(entity)
        await self.unit_of_work.commit()
        
        return entity
    
    async def update(self, entity: T):
        self._set_update_audit_fields(entity)
        self.db_session.merge(entity)
        await self.unit_of_work.commit()
        
        return entity
    
    async def delete(self, entity: T):
        self._set_delete_audit_fields(entity)
        await self.db_session.delete(entity)
        await self.unit_of_work.commit()

    async def add_range(self, entities: List[T]):
        for entity in entities:
            self._set_create_audit_fields(entity)
        
        self.db_session.add_all(entities)
        await self.unit_of_work.commit()
        
        return entities
    
    async def update_range(self, entities: List[T]):
        for entity in entities:
            self._set_update_audit_fields(entity)
            await self.db_session.merge(entity)
            
        await self.unit_of_work.commit()
        
        return entities

    async def delete_range(self, entities: List[T]):
        for entity in entities:
            self._set_delete_audit_fields(entity)
            await self.db_session.delete(entity)
        await self.unit_of_work.commit()
