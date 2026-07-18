from dependency_injector.providers import Provider

from shared.src.data.db_session_base import DbSessionBase
from shared.src.data.interfaces.db_session import IDbSession


class ObjectRecognitionDbSession(DbSessionBase):
    def __init__(self, db_session: IDbSession):
        super().__init__(db_session)    