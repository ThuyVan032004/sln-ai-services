from shared.data.interfaces import IUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWorkBase(IUnitOfWork):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def commit(self):
        await self.db_session.commit()

    async def rollback(self):
        await self.db_session.rollback()
    
    async def close(self):
        await self.db_session.close()
        
    