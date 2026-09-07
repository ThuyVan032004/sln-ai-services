from shared.business import DomainServiceBase
from shared.data.interfaces import IRepository


class ObjectRecognitionDomainService[T](DomainServiceBase[T]):
    def __init__(self, repository: IRepository[T]):
        super().__init__(repository)