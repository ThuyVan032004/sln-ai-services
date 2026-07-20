from shared.business.domain_service_base import DomainServiceBase
from shared.data.interfaces.repository import IRepository
from shared.data.interfaces.unit_of_work import IUnitOfWork


class ObjectRecognitionDomainService(DomainServiceBase):
    def __init__(self, repository: IRepository):
        super().__init__(repository)