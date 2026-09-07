from object_recognition_service.data.entities import Category
from shared.data.interfaces import IRepository
from dependency_injector.wiring import inject, Provide

from object_recognition_service.business import ObjectRecognitionDomainService
from object_recognition_service.host.container import container

class CategoryManager(ObjectRecognitionDomainService[Category]):
    @inject
    def __init__(self, repository: IRepository[Category] = Provide[container.repository.add_kwargs(entity_type=Category)]):
        super().__init__(repository)