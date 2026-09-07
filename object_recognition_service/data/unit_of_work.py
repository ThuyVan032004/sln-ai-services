from shared.data.interfaces import IDbSession
from shared.data import UnitOfWorkBase


class ObjectRecognitionUnitOfWork(UnitOfWorkBase):
    def __init__(self, db_session: IDbSession):
        super().__init__(db_session)