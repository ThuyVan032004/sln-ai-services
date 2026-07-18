import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from shared.src.common.constants.env_constants import EnvConstants
from shared.src.data.interfaces.db_session import IDbSession

class DbSessionBase(IDbSession):
    def __init__(self):
        database_url = os.getenv(EnvConstants.DATABASE_URL)
        
        if not database_url:
            raise ValueError(f"Environment variable '{EnvConstants.DATABASE_URL}' is not set.")
        
        self._engine = create_async_engine(database_url, echo=False)
        
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    def get_session(self) -> AsyncSession:
        return self._session_factory()