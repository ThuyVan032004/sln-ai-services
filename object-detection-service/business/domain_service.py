from dependency_injector.providers import Provider

from shared.src.business.domain_service_base import DomainServiceBase
from shared.src.data.interfaces.repository import IRepository
from shared.src.data.interfaces.unit_of_work import IUnitOfWork


class ObjectDetectionDomainService(DomainServiceBase):
    def __init__(self, repository: Provider[IRepository], unit_of_work: Provider[IUnitOfWork]):
        super().__init__(repository, unit_of_work)