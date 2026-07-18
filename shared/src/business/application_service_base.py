
from dependency_injector.providers import Provider

from shared.src.business.interfaces.application_service import IApplicationService
from shared.src.business.interfaces.domain_service import IDomainService


class ApplicationServiceBase(IApplicationService):
    def get_service(self, domain_service: IDomainService):
        return domain_service
        
        
        