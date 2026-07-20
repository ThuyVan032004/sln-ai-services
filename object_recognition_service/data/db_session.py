from dependency_injector.providers import Provider

from shared.data.db_session_base import DbSessionBase
from shared.data.interfaces.db_session import IDbSession


class ObjectRecognitionDbSession(DbSessionBase):
    def __init__(self):
        super().__init__()    