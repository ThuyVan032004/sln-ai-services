from shared.data.interfaces import IUnitOfWork
from shared.business.interfaces import IApplicationService


class ApplicationServiceBase(IApplicationService):
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work