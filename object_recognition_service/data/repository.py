from typing import Type

from shared.data.interfaces import IDbSession
from shared.data import RepositoryBase


class ObjectRecognitionRepository[T](RepositoryBase[T]):
    def __init__(self, db_session: IDbSession, entity_type: Type[T]):
        super().__init__(db_session, entity_type)