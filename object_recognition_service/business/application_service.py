from shared.data.interfaces import IUnitOfWork
from shared.business import ApplicationServiceBase


class ObjectRecognitionApplicationService(ApplicationServiceBase):
    def __init__(self, unit_of_work: IUnitOfWork):
        super().__init__(unit_of_work)