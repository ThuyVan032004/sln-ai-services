from object_recognition_service.data.entities import Model
from shared.data.interfaces import IRepository
from dependency_injector.wiring import inject, Provide

from object_recognition_service.business import ObjectRecognitionDomainService
from object_recognition_service.host import container

class ModelManager(ObjectRecognitionDomainService[Model]):
    @inject
    def __init__(self, repository: IRepository[Model] = Provide[container.repository.add_kwargs(entity_type=Model)]):
        super().__init__(repository)