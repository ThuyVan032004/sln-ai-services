from data.entities.image import Image
from data.repository import ObjectRecognitionRepository
from dependency_injector.wiring import inject, Provide

from object_recognition_service.business.domain_service import ObjectRecognitionDomainService
from host.container import container


class ImageManager(ObjectRecognitionDomainService):
    @inject
    def __init__(self, repository: ObjectRecognitionRepository[Image] = Provide[container.image_repository]):
        super().__init__(repository)