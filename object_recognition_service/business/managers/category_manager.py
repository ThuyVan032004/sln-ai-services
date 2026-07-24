from data.entities.category import Category
from data.repository import ObjectRecognitionRepository
from dependency_injector.wiring import inject, Provide

from business.domain_service import ObjectRecognitionDomainService
from host.container import container

class CategoryManager(ObjectRecognitionDomainService):
    @inject
    def __init__(self, repository: ObjectRecognitionRepository[Category] = Provide[container.category_repository]):
        super().__init__(repository)