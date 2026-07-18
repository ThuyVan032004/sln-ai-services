from dependency_injector.wiring import inject, Provide

from object_recognition_service.business.domain_service import ObjectRecognitionDomainService


class ImageManager(ObjectRecognitionDomainService):
    @inject
    def __init__(self, repository = Provide["repository"]):
        super().__init__(repository)