from dependency_injector.wiring import inject, Provide

from business.domain_service import ObjectRecognitionDomainService
from host.container import container

class ImageManager(ObjectRecognitionDomainService):
    @inject
    def __init__(self, repository = Provide[container.repository]):
        super().__init__(repository)