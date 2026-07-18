from shared.src.business.domain_service_base import DomainServiceBase
from shared.src.data.interfaces.repository import IRepository
from shared.src.data.interfaces.unit_of_work import IUnitOfWork


class ObjectRecognitionDomainService(DomainServiceBase):
    def __init__(self, repository: IRepository):
        super().__init__(repository)