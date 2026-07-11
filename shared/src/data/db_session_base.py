from contextlib import asynccontextmanager
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from shared.src.common.constants.env_constants import EnvConstants
from shared.src.data.interfaces.db_session import IDbSession

class DbSessionBase(IDbSession):
    @asynccontextmanager
    async def get_session(self) -> AsyncSession:
        database_url = os.getenv(EnvConstants.DATABASE_URL)
        
        if not database_url:
            raise ValueError(f"Environment variable '{EnvConstants.DATABASE_URL}' is not set.")
        
        engine = create_async_engine(database_url, echo=False)
        return async_sessionmaker(engine, expire_on_commit=False)