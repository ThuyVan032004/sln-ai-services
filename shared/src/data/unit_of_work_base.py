from shared.src.data.interfaces.db_session import IDbSession
from shared.src.data.interfaces.unit_of_work import IUnitOfWork
from dependency_injector.providers import Provider


class UnitOfWorkBase(IUnitOfWork):
    def __init__(self, db_session: Provider[IDbSession]):
        self.db_session = db_session()
        
    async def commit(self):
        await self.db_session.commit()

    async def rollback(self):
        await self.db_session.rollback()
        
    