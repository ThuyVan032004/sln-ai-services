from dependency_injector.providers import Provider
from shared.src.data.interfaces.unit_of_work import IUnitOfWork

from shared.src.business.application_service_base import ApplicationServiceBase
from shared.src.business.interfaces.domain_service import IDomainService


class ObjectRecognitionApplicationService(ApplicationServiceBase):
    def __init__(self, unit_of_work: IUnitOfWork):
        super().__init__(unit_of_work)