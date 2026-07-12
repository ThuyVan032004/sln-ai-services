from dependency_injector.providers import Provider

from shared.src.business.application_service_base import ApplicationServiceBase
from shared.src.business.interfaces.domain_service import IDomainService


class ObjectDetectionApplicationService(ApplicationServiceBase):
    def __init__(self, domain_service: Provider[IDomainService]):
        super().__init__(domain_service)