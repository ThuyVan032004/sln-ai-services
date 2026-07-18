from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide
from fastapi import Depends
# from host.container import container

from object_recognition_service.contracts.image.create_image_request import CreateImageRequest, CreateImageResponse
from object_recognition_service.business.services.image_service import ImageService


class CreateImageRequestHandler(RequestHandler[CreateImageRequest, CreateImageResponse]):
    @inject
    def __init__(self, image_service: ImageService = Depends(Provide["image_service"])):
        self.image_service = image_service
        
    async def handle(self, request: CreateImageRequest) -> CreateImageResponse:
        return await self.image_service.create(request)