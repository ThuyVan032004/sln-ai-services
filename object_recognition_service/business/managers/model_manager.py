from data.entities.model import Model
from data.repository import ObjectRecognitionRepository
from dependency_injector.wiring import inject, Provide

from business.domain_service import ObjectRecognitionDomainService
from object_recognition_service.host.container import container

class ModelManager(ObjectRecognitionDomainService):
    @inject
    def __init__(self, repository: ObjectRecognitionRepository[Model] = Provide[container.model_repository]):
        super().__init__(repository)