from datetime import datetime
from typing import List, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from shared.data.interfaces import IRepository


class RepositoryBase[T](IRepository[T]):
    def __init__(self, db_session: AsyncSession, entity_type: Type[T]):
        self.db_session = db_session
        self._entity_type = entity_type

    def _set_create_audit_fields(self, entity: T):
        entity.created_at = datetime.now()
        entity.is_deleted = False

    def _set_update_audit_fields(self, entity: T):
        entity.updated_at = datetime.now()

    def _set_delete_audit_fields(self, entity: T):
        entity.deleted_at = datetime.now()
        entity.is_deleted = True

    async def get_all(self):
        result = await self.db_session.execute(select(self._entity_type))
        return result.scalars().all()

    async def find_by(self, filter):
        result = await self.db_session.execute(select(self._entity_type).where(filter))
        return result.scalars().first()

    async def add(self, entity: T):
        self._set_create_audit_fields(entity)
        self.db_session.add(entity)
        return entity

    async def update(self, entity: T):
        self._set_update_audit_fields(entity)
        # Fix: thêm await cho merge
        return await self.db_session.merge(entity)

    async def delete(self, entity: T):
        self._set_delete_audit_fields(entity)
        # Fix: thêm await cho merge
        return await self.db_session.merge(entity)

    async def add_range(self, entities: List[T]):
        for entity in entities:
            self._set_create_audit_fields(entity)

        self.db_session.add_all(entities)
        return entities

    async def update_range(self, entities: List[T]):
        for entity in entities:
            self._set_update_audit_fields(entity)
            # Fix: thêm await cho merge
            await self.db_session.merge(entity)

        return entities

    async def delete_range(self, entities: List[T]):
        for entity in entities:
            self._set_delete_audit_fields(entity)
            # Fix: thêm await cho merge
            await self.db_session.merge(entity)