from dependency_injector.wiring import inject, Provide

from business.application_service import ObjectRecognitionApplicationService
from contracts.image.create_image_request import CreateImageRequest, CreateImageResponse
from host.container import container

class ImageService(ObjectRecognitionApplicationService):
    @inject
    def __init__(self, image_manager = Provide[container.image_manager]):
        self.image_manager = image_manager

    async def create(self, request: CreateImageRequest) -> CreateImageResponse:
        return await self.image_manager.create(request)
