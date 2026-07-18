
from dependency_injector.providers import Provider
from src.data.interfaces.unit_of_work import IUnitOfWork

from shared.src.business.interfaces.application_service import IApplicationService
from shared.src.business.interfaces.domain_service import IDomainService


class ApplicationServiceBase(IApplicationService):
    def __init__(self, unit_of_work: IUnitOfWork):
        self.unit_of_work = unit_of_work
        
        
        