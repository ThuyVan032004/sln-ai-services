from dependency_injector.providers import Provider
from shared.data.interfaces.unit_of_work import IUnitOfWork

from shared.business.application_service_base import ApplicationServiceBase
from shared.business.interfaces.domain_service import IDomainService


class ObjectRecognitionApplicationService(ApplicationServiceBase):
    def __init__(self, unit_of_work: IUnitOfWork):
        super().__init__(unit_of_work)