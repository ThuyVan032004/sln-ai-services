from dependency_injector.providers import Provider

from shared.src.data.interfaces.unit_of_work import IUnitOfWork
from shared.src.data.interfaces.db_session import IDbSession
from shared.src.data.repository_base import RepositoryBase


class ObjectRecognitionRepository[T](RepositoryBase[T]):
    def __init__(self, db_session: IDbSession):
        super().__init__(db_session)