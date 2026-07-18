from dependency_injector.providers import Provider

from shared.src.data.interfaces.db_session import IDbSession
from shared.src.data.unit_of_work_base import UnitOfWorkBase


class ObjectRecognitionUnitOfWork(UnitOfWorkBase):
    def __init__(self, db_session: IDbSession):
        super().__init__(db_session)